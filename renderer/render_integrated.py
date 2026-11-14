#!/usr/bin/env python3
"""Render the articulated Canvas rig into a real MP4 with narration and sound.

This is the first executable integration path for the rig prototype: the HTML
canvas owns the character IK, environment, camera move and captions; Playwright
samples it frame-by-frame; FFmpeg encodes video and muxes narration.
"""
from pathlib import Path
import subprocess
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "experiments" / "2026-11-14" / "rig-benchmark-v2.html"
OUTDIR = ROOT / "renders" / "integrated"
FRAMES = OUTDIR / "frames"
FPS = 24
DURATION = 12
WIDTH, HEIGHT = 1920, 1080
OUTDIR.mkdir(parents=True, exist_ok=True)
FRAMES.mkdir(parents=True, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    if not HTML.exists():
        raise FileNotFoundError(HTML)
    for p in FRAMES.glob("frame_*.png"):
        p.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
        page.goto(HTML.as_uri(), wait_until="load")
        page.wait_for_function("typeof window.renderAt === 'function'")
        for frame in range(FPS * DURATION):
            t = frame / FPS
            page.evaluate("(t) => window.renderAt(t)", t)
            page.locator("#c").screenshot(path=str(FRAMES / f"frame_{frame:05d}.png"))
        browser.close()

    narration = (
        "A small distraction changes your direction. "
        "Your body commits before your attention catches up. "
        "You can choose where the next step goes."
    )
    wav = OUTDIR / "narration.wav"
    run(["espeak-ng", "-v", "en-us", "-s", "145", "-w", str(wav), narration])
    mp4 = OUTDIR / "wise-lab-integrated-rig-12sec.mp4"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", str(FPS), "-i", str(FRAMES / "frame_%05d.png"),
        "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "scale=1280:720:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "160k",
        "-af", "apad", "-t", str(DURATION), "-movflags", "+faststart", str(mp4)
    ])
    print(f"INTEGRATED_RENDER_OK: {mp4} ({FPS*DURATION} frames, {WIDTH}x{HEIGHT} source)")

if __name__ == "__main__":
    main()
