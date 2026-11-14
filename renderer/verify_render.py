"""Validate the benchmark MP4's streams, resolution and duration."""
import json
import subprocess
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "renders/wise-lab-production-character-20sec.mp4")
if not path.is_file() or path.stat().st_size < 50_000:
    raise SystemExit(f"FAIL: missing or unexpectedly small MP4: {path}")
probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries",
    "format=duration:stream=codec_type,width,height,codec_name",
    "-of", "json", str(path)
], check=True, capture_output=True, text=True)
data = json.loads(probe.stdout)
streams = data.get("streams", [])
video = next((s for s in streams if s.get("codec_type") == "video"), None)
audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
duration = float(data.get("format", {}).get("duration", 0))
assert video and video.get("width") == 1280 and video.get("height") == 720, data
assert audio, f"No audio stream: {data}"
assert 11.8 <= duration <= 12.2, f"Unexpected duration {duration:.2f}s"
print(f"PASS: {path} | {video['width']}x{video['height']} | {duration:.2f}s | video={video['codec_name']} audio={audio['codec_name']}")
