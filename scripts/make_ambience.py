#!/usr/bin/env python3
"""Create an original, quiet cinematic bed with soft transition swells (no external assets)."""
import math, random, struct, wave
from pathlib import Path

RATE = 24000
DURATION = 60
random.seed(17)
out = Path("public/ambience.wav")
out.parent.mkdir(parents=True, exist_ok=True)
previous = 0.0
with wave.open(str(out), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(RATE)
    chunk = bytearray()
    for i in range(RATE * DURATION):
        t = i / RATE
        fade = min(1.0, t / 2.0, (DURATION - t) / 2.0)
        slow = 0.72 + 0.28 * math.sin(2 * math.pi * t / 17.0)
        pad = (0.105 * math.sin(2 * math.pi * 82.41 * t)
               + 0.065 * math.sin(2 * math.pi * 110.0 * t + 0.3 * math.sin(t / 4))
               + 0.035 * math.sin(2 * math.pi * 164.81 * t))
        # Four restrained airy swells mark the scene changes without masking speech.
        swell = 0.0
        for start in (14.7, 29.7, 44.7):
            age = t - start
            if 0 <= age <= 1.5:
                env = math.sin(math.pi * age / 1.5) ** 2
                noise = random.uniform(-1, 1)
                previous = 0.88 * previous + 0.12 * noise
                swell += previous * env * 0.11
        sample = max(-0.28, min(0.28, (pad * slow + swell) * fade))
        chunk.extend(struct.pack("<h", int(sample * 32767)))
        if len(chunk) >= 96000:
            wav.writeframesraw(chunk)
            chunk.clear()
    if chunk:
        wav.writeframesraw(chunk)
print(f"Created {out} ({RATE} Hz, {DURATION}s)")
