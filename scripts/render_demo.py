import argparse
import asyncio
import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "prototype" / "index.html"


async def render(output: Path, seconds: float, fps: int, width: int, height: int) -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to encode the MP4")
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="wise-lab-frames-") as tmp:
        frames = Path(tmp)
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                reduced_motion="reduce",
            )
            await page.goto(HTML.as_uri(), wait_until="load")
            await page.evaluate("document.fonts.ready")
            total = round(seconds * fps)
            for frame in range(total):
                timestamp = frame / fps
                await page.evaluate("(t) => window.renderAt(t)", timestamp)
                await page.screenshot(path=str(frames / f"frame_{frame:06d}.png"))
                if frame % fps == 0:
                    print(f"Rendered {frame}/{total} frames ({timestamp:.1f}s)", flush=True)
            await browser.close()

        command = [
            "ffmpeg", "-y", "-framerate", str(fps),
            "-i", str(frames / "frame_%06d.png"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output),
        ]
        subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the WISE-LAB motion lab prototype.")
    parser.add_argument("--output", default="dist/wise-lab-motion-test.mp4")
    parser.add_argument("--seconds", type=float, default=12)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()
    if args.seconds <= 0 or args.fps <= 0 or args.width <= 0 or args.height <= 0:
        parser.error("seconds, fps, width, and height must be positive")
    asyncio.run(render(Path(args.output).resolve(), args.seconds, args.fps, args.width, args.height))


if __name__ == "__main__":
    main()
