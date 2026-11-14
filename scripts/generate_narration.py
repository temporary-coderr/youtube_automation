#!/usr/bin/env python3
"""Generate narration audio and word-timed SRT captions using free Edge TTS."""
import asyncio
import re
import subprocess
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "scripts/narration.txt").read_text(encoding="utf-8").strip()
AUDIO = ROOT / "public/narration.mp3"
SRT = ROOT / "public/captions.srt"
VOICE = "en-US-AndrewNeural"

def stamp(seconds):
    ms = max(0, round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

async def generate():
    comm = edge_tts.Communicate(TEXT, VOICE, rate="-5%")
    words = []
    with AUDIO.open("wb") as audio:
        async for part in comm.stream():
            if part["type"] == "audio":
                audio.write(part["data"])
            elif part["type"] == "WordBoundary":
                start = part["offset"] / 10_000_000
                end = start + part["duration"] / 10_000_000
                token = part["text"].strip()
                if token:
                    words.append((start, end, token))
    if not words or not AUDIO.exists() or AUDIO.stat().st_size < 1000:
        raise RuntimeError("Edge TTS returned no usable word timings")
    # Readable two-line-safe captions: group 5-8 words, max ~3.2 seconds.
    groups, current = [], []
    for word in words:
        current.append(word)
        phrase = " ".join(x[2] for x in current)
        if len(current) >= 7 or (len(current) >= 4 and word[1] - current[0][0] >= 2.8) or phrase.endswith((".", "?", "!")):
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    lines = []
    for i, group in enumerate(groups, 1):
        phrase = " ".join(x[2] for x in group)
        # Split long phrases at the nearest word to the midpoint.
        if len(phrase) > 48 and len(group) >= 5:
            mid = len(group) // 2
            phrase = " ".join(x[2] for x in group[:mid]) + "\\N" + " ".join(x[2] for x in group[mid:])
        lines += [str(i), f"{stamp(group[0][0])} --> {stamp(group[-1][1] + 0.12)}", phrase.replace("\\N", "\n"), ""]
    SRT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {AUDIO} and {SRT} from {len(words)} word timings")

if __name__ == "__main__":
    try:
        asyncio.run(generate())
    except Exception as exc:
        print(f"Edge TTS unavailable; creating offline narration and estimated SRT: {exc}")
        wav = ROOT / "public/narration.wav"
        subprocess.run(["espeak-ng", "-v", "en-us", "-s", "138", "-f", str(ROOT / "scripts/narration.txt"), "-w", str(wav)], check=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav), str(AUDIO)], check=True)
        duration = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(AUDIO)], text=True).strip())
        tokens = re.findall(r"\\S+", TEXT)
        groups = [tokens[i:i+7] for i in range(0, len(tokens), 7)]
        total = sum(len(x) for x in tokens) or 1
        cursor, lines = 0.0, []
        for i, group in enumerate(groups, 1):
            span = duration * sum(len(x) for x in group) / total
            lines += [str(i), f"{stamp(cursor)} --> {stamp(cursor + span)}", " ".join(group), ""]
            cursor += span
        SRT.write_text("\\n".join(lines), encoding="utf-8")
