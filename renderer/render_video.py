#!/usr/bin/env python3
"""Deterministic HTML/SVG scene renderer for WISE-LAB.

This is the first production-rendering adapter: scene animation is evaluated at
an explicit timestamp, captured frame-by-frame by Chromium, then encoded by
FFmpeg. It intentionally fails fast rather than silently producing partial MP4s.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", default="prototype/index.html")
    parser.add_argument("--output", default="output/wise-lab-preview.mp4")
    parser.add_argument("--duration", type=float, default=12.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--audio", default=None, help="Optional narration/music file")
    parser.add_argument("--crf", type=int, default=18)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scene = Path(args.scene).resolve()
    output = Path(args.output).resolve()
    if not scene.is_file():
        raise SystemExit(f"Scene file does not exist: {scene}")
    if args.duration <= 0 or args.fps <= 0 or args.width <= 0 or args.height <= 0:
        raise SystemExit("Duration, FPS, width and height must all be positive")
    if not 0 <= args.crf <= 51:
        raise SystemExit("CRF must be between 0 and 51")
    if not shutil.which("ffmpeg"):
        raise SystemExit("FFmpeg is required but was not found on PATH")
    audio = Path(args.audio).resolve() if args.audio else None
    if audio and not audio.is_file():
        raise SystemExit(f"Audio file does not exist: {audio}")

    output.parent.mkdir(parents=True, exist_ok=True)
    total_frames = round(args.duration * args.fps)
    with tempfile.TemporaryDirectory(prefix="wise-lab-frames-") as temp:
        frames = Path(temp)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(
                viewport={"width": args.width, "height": args.height},
                device_scale_factor=1,
                reduced_motion="reduce",
            )
            page.goto(scene.as_uri(), wait_until="networkidle")
            page.wait_for_function("typeof window.renderAt === 'function'")
            for frame in range(total_frames):
                timestamp = frame / args.fps
                page.evaluate("(t) => window.renderAt(t)", timestamp)
                page.screenshot(
                    path=str(frames / f"frame-{frame:06d}.png"),
                    animations="disabled",
                )
                if frame % max(1, args.fps * 5) == 0:
                    print(f"Rendered {frame}/{total_frames} frames ({timestamp:.1f}s)")
            browser.close()

        video_input = [
            "ffmpeg", "-hide_banner", "-y",
            "-framerate", str(args.fps),
            "-i", str(frames / "frame-%06d.png"),
        ]
        if audio:
            command = video_input + [
                "-i", str(audio),
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-af", "apad", "-t", str(args.duration),
                "-movflags", "+faststart", str(output),
            ]
        else:
            command = video_input + [
                "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
                "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
                str(output),
            ]
        run(command)

    if not output.is_file() or output.stat().st_size == 0:
        raise SystemExit("FFmpeg did not produce a valid MP4")
    print(f"SUCCESS: {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
