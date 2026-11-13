#!/usr/bin/env python3
"""Render the layered SVG motion study to a validated MP4 using deterministic timestamps."""
from __future__ import annotations
import argparse, asyncio, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = ROOT / "prototype" / "index.html"
DEFAULT_OUTPUT = ROOT / "renders" / "cinematic-preview.mp4"

def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()

async def render_frames(html: Path, frame_dir: Path, width: int, height: int, fps: int, duration: float) -> int:
    total = int(round(fps * duration))
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1, reduced_motion="reduce")
        page.set_default_timeout(30_000)
        await page.goto(html.resolve().as_uri(), wait_until="load")
        await page.wait_for_function("typeof window.renderAt === 'function'")
        # The source scene is authored in 16:9. For portrait output, use a real
        # center crop around the lead character instead of squashing the artwork.
        if height > width:
            crop_width = 1080 * width / height
            crop_x = 720 - crop_width / 2
            await page.evaluate("""({x, w}) => {
                const frame = document.getElementById('frame');
                const svg = document.querySelector('svg');
                frame.style.width = '100vw';
                frame.style.height = '100vh';
                svg.setAttribute('viewBox', x + ' 0 ' + w + ' 1080');
            }""", {"x": crop_x, "w": crop_width})
        await page.add_style_tag(content="*,*::before,*::after{animation:none!important;transition:none!important;}")
        for index in range(total):
            timestamp = index / fps
            await page.evaluate("(t) => window.renderAt(t)", timestamp)
            await page.screenshot(path=str(frame_dir / f"frame_{index:06d}.png"), animations="disabled", type="png")
            if index % max(1, fps * 2) == 0:
                print(f"Rendered {index + 1}/{total} frames ({timestamp:.1f}s)", flush=True)
        await browser.close()
    return total

def encode(frame_dir: Path, output: Path, fps: int, duration: float, audio: Path | None, crf: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(fps),
           "-i", str(frame_dir / "frame_%06d.png")]
    if audio:
        cmd += ["-i", str(audio)]
    cmd += ["-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if audio:
        cmd += ["-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    else:
        cmd += ["-an"]
    cmd.append(str(output))
    run(cmd)

def validate(output: Path, width: int, height: int) -> dict:
    raw = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=codec_name,width,height,r_frame_rate",
               "-show_entries", "format=duration,size", "-of", "json", str(output)])
    data = json.loads(raw)
    stream, duration, size = data["streams"][0], float(data["format"]["duration"]), int(data["format"]["size"])
    if stream["codec_name"] != "h264":
        raise RuntimeError(f"Unexpected codec: {stream['codec_name']}")
    if (stream["width"], stream["height"]) != (width, height):
        raise RuntimeError(f"Unexpected dimensions: {stream['width']}x{stream['height']}")
    if duration <= 0 or size < 10_000:
        raise RuntimeError(f"Invalid output (duration={duration}, bytes={size})")
    return {"status":"passed","file":str(output),"codec":stream["codec_name"],"width":width,
            "height":height,"fps":stream["r_frame_rate"],"duration_seconds":duration,"size_bytes":size}

async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=12.0)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()
    if not args.html.is_file():
        raise FileNotFoundError(f"Scene HTML not found: {args.html}")
    if args.width < 320 or args.height < 180 or args.fps < 1 or args.duration <= 0 or args.duration > 12:
        raise ValueError("Invalid dimensions or frame rate; this authored prototype supports 0 < duration <= 12 seconds")
    if args.audio and not args.audio.is_file():
        raise FileNotFoundError(f"Audio not found: {args.audio}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe must be installed on PATH")
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="wise-lab-frames-") as tmp:
        frame_dir = Path(tmp)
        total = await render_frames(args.html, frame_dir, args.width, args.height, args.fps, args.duration)
        encode(frame_dir, args.output.resolve(), args.fps, args.duration, args.audio, args.crf)
        report = validate(args.output.resolve(), args.width, args.height)
        report["frames_rendered"] = total
        report["render_seconds"] = round(time.time() - started, 2)
        report_path = args.output.resolve().with_suffix(".report.json")
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2), flush=True)
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as exc:
        print(f"RENDER FAILED: {exc}", file=sys.stderr, flush=True)
        raise
