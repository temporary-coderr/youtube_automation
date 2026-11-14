#!/usr/bin/env python3
"""WISE-LAB animal story renderer: illustrated 2D cutout rigs + 2.5D camera.

A short, original forest fable rendered with CairoSVG/Pillow and FFmpeg.  The
characters use layered SVG paths, articulated limb groups, procedural blinks,
head/ear/tail motion, prop interaction, parallax scenery and camera tracks.
"""
from __future__ import annotations
import html
import json
import math
import os
import random
import shutil
import subprocess
import tempfile
import wave
from array import array
from pathlib import Path

import cairosvg
from PIL import Image
from io import BytesIO

W, H, FPS, OUTPUT_FPS = 1280, 720, 12, 24
ROOT = Path("renders/animal-2d")
ROOT.mkdir(parents=True, exist_ok=True)
MP4 = ROOT / "wise-lab-fox-and-turtle.mp4"
SRT = ROOT / "captions.srt"
REPORT = ROOT / "render-report.json"
CONTACT = ROOT / "contact-sheet.jpg"
NARRATION = ROOT / "narration.wav"
AMBIENCE = ROOT / "forest-ambience.wav"

STORY = [
    {"caption": "Finn the fox hurried home with a basket of berries.",
     "title": "A JOURNEY THROUGH THE WOODS"},
    {"caption": "A splash stopped him beside the little forest stream.",
     "title": "A SURPRISING SOUND"},
    {"caption": "Olive the turtle was stranded on a slippery stone.",
     "title": "A FRIEND IN TROUBLE"},
    {"caption": "Finn rolled a fallen branch into a steady bridge.",
     "title": "A LITTLE HELP"},
    {"caption": "Olive crossed slowly, while Finn steadied the log.",
     "title": "ONE CAREFUL STEP AT A TIME"},
    {"caption": "Together, they found that kindness makes a path.",
     "title": "A FRIENDSHIP BEGINS"},
]


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def ease(v: float) -> float:
    v = clamp(v)
    return v * v * (3.0 - 2.0 * v)


def mix(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def blink(t: float, offset: float = 0.0) -> float:
    # Mostly-open eye, with a few short full blinks per story.
    phase = (t + offset) % 3.7
    if phase < 0.12:
        return max(0.08, phase / 0.12)
    if phase > 3.56:
        return max(0.08, (3.7 - phase) / 0.14)
    return 1.0


def find_tts() -> str:
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        raise RuntimeError("Install espeak-ng (or espeak) to create the free offline narration.")
    return exe


def srt_time(seconds: float) -> str:
    ms = int(round(max(0.0, seconds) * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def make_narration() -> tuple[list[float], float]:
    exe = find_tts()
    temp = ROOT / "voice_parts"
    temp.mkdir(exist_ok=True)
    parts: list[bytes] = []
    durations: list[float] = []
    params: tuple[int, int, int] | None = None
    silence_seconds = 0.18
    silence_frames = 0
    for i, scene in enumerate(STORY):
        wav_path = temp / f"line_{i+1:02d}.wav"
        cmd = [exe, "-v", "en-us+m3", "-s", "150", "-a", "155", "-w", str(wav_path), scene["caption"]]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with wave.open(str(wav_path), "rb") as wf:
            current = (wf.getnchannels(), wf.getsampwidth(), wf.getframerate())
            if params is None:
                params = current
            if current != params:
                raise RuntimeError(f"Unexpected narration WAV format: {current} != {params}")
            frames = wf.readframes(wf.getnframes())
        assert params is not None
        channels, width, rate = params
        frames_count = len(frames) // (channels * width)
        duration = frames_count / rate
        parts.append(frames)
        durations.append(duration)
        if i < len(STORY) - 1:
            silence_frames = int(rate * silence_seconds)
            parts.append(b"\x00" * silence_frames * channels * width)
            durations[-1] += silence_seconds
    if params is None:
        raise RuntimeError("No narration lines were generated.")
    with wave.open(str(NARRATION), "wb") as out:
        out.setnchannels(params[0]); out.setsampwidth(params[1]); out.setframerate(params[2])
        out.writeframes(b"".join(parts))
    # Timings use measured voice durations, not guessed words-per-minute.
    start = 0.0
    cues = []
    for i, (scene, duration) in enumerate(zip(STORY, durations)):
        spoken_end = start + duration - (silence_seconds if i < len(STORY) - 1 else 0.0)
        cues.extend([str(i + 1), f"{srt_time(start)} --> {srt_time(spoken_end)}", scene["caption"], ""])
        start += duration
    SRT.write_text("\n".join(cues), encoding="utf-8")
    total = sum(durations)
    (ROOT / "narration.txt").write_text("\n".join(s["caption"] for s in STORY), encoding="utf-8")
    print(f"Narration created with {exe}: {total:.2f}s, {len(STORY)} measured subtitle cues", flush=True)
    return durations, total


def make_ambience(duration: float) -> None:
    """Procedural quiet forest bed with stream noise and occasional bird chirps."""
    rate = 22050
    n = int(rate * duration)
    rng = random.Random(241114)
    # Simple smoothed noise bed plus quiet tones; low enough to sit below narration.
    noise = 0.0
    pcm = array("h")
    chirps = [2.1, 6.4, 10.7, 15.2, 19.6]
    thumps = [durations for durations in ()]  # explicit empty event list keeps synthesis deterministic
    for i in range(n):
        t = i / rate
        noise = noise * 0.93 + rng.uniform(-1.0, 1.0) * 0.07
        wind = noise * 0.010
        stream = (0.007 * math.sin(2 * math.pi * 118 * t) + 0.004 * math.sin(2 * math.pi * 177 * t))
        bird = 0.0
        for start in chirps:
            u = t - start
            if 0 <= u <= 0.42:
                env = math.sin(math.pi * u / 0.42) ** 2
                freq = 2050 + 500 * math.sin(u * 8.0)
                bird += 0.012 * env * math.sin(2 * math.pi * freq * u)
        # Gentle woody roll/footfall accents around the bridge-building beat.
        fx = 0.0
        for start, amp, length in ((8.8, 0.04, 0.20), (9.15, 0.025, 0.14), (14.2, 0.018, 0.10)):
            u = t - start
            if 0 <= u <= length:
                fx += amp * math.exp(-u * 18) * math.sin(2 * math.pi * (90 + 20 * u) * u)
        value = max(-0.9, min(0.9, wind + stream + bird + fx))
        pcm.append(int(value * 32767))
    with wave.open(str(AMBIENCE), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(rate); out.writeframes(pcm.tobytes())


def fox_svg(x: float, ground: float, t: float, scene: int, u: float) -> str:
    # Fox walks in, notices Turtle, pushes the log, then escorts his new friend.
    if scene == 0:
        root_x = mix(325, 500, ease(u)); stride = 1.0 - ease(u * 0.95)
    elif scene in (1, 2):
        root_x = 500 if scene == 1 else mix(500, 625, ease(u))
        stride = 0.0 if scene == 1 else 0.35 * (1.0 - ease(u))
    elif scene in (3, 4):
        root_x = 625; stride = 0.0
    else:
        root_x = mix(625, 400, ease(u)); stride = 0.85
    phase = t * 7.8
    bob = abs(math.sin(phase)) * 5.0 * stride
    tail = 8 * math.sin(t * 3.8) + (7 if scene == 1 else 0)
    head_turn = 0
    if scene == 1: head_turn = -13 * ease(u)
    elif scene == 2: head_turn = -10 + 4 * math.sin(u * math.pi)
    elif scene == 3: head_turn = -4 * (1 - ease(u))
    elif scene == 4: head_turn = -5
    elif scene == 5: head_turn = -2
    paw_push = ease(u) if scene == 3 else (1 - ease(u)) if scene == 4 else 0
    crouch = 7 * ease(u) if scene in (2, 3) else (7 * (1 - ease(u)) if scene == 4 else 0)
    b = blink(t, .4)
    f = []
    f.append(f'<g id="finn" transform="translate({root_x:.2f} {ground+bob+crouch:.2f})">')
    f.append('<ellipse cx="-20" cy="-3" rx="168" ry="22" fill="#142b29" opacity=".28" filter="url(#softShadow)"/>')
    # Bushy tail, a separate articulated layer with cream tip and fur striations.
    f.append(f'<g transform="rotate({tail:.2f} -82 -118)">')
    f.append('<path d="M-72 -116 C-118 -190 -220 -205 -272 -154 C-312 -114 -278 -45 -223 -42 C-168 -39 -121 -76 -72 -91Z" fill="url(#foxFur)" stroke="#713b24" stroke-width="8" stroke-linejoin="round"/>')
    f.append('<path d="M-266 -153 C-254 -185 -212 -187 -184 -168 C-206 -148 -208 -119 -187 -88 C-230 -84 -274 -111 -266 -153Z" fill="#f5e4c4" stroke="#b76d3e" stroke-width="5"/>')
    f.append('<path d="M-255 -147Q-217 -166 -193 -147M-248 -119Q-217 -135 -194 -118M-222 -84Q-201 -102 -178 -100" fill="none" stroke="#c76f39" stroke-width="5" opacity=".7" stroke-linecap="round"/>')
    f.append('</g>')
    # Far legs (behind the body) with articulated gait cycles.
    for idx, lx in enumerate((-76, 55)):
        a = math.sin(phase + (idx * math.pi)) * 22 * stride
        f.append(f'<g transform="translate({lx} -87) rotate({a:.2f})">')
        f.append('<path d="M-13 -2 Q-23 29 -17 62 Q-15 78 0 79 Q15 77 13 61 L9 5Z" fill="url(#foxFur)" stroke="#743f28" stroke-width="6"/>')
        f.append('<path d="M-12 57Q-4 64 11 58" fill="none" stroke="#f5c08a" stroke-width="4"/>')
        f.append('<path d="M-8 72Q-23 75 -24 87Q-20 98 3 97Q25 98 24 85Q17 73 7 73Z" fill="#c96d36" stroke="#743f28" stroke-width="5"/>')
        f.append('<path d="M-9 88L-5 93M4 88L8 93" stroke="#f7d6a9" stroke-width="3" stroke-linecap="round"/>')
        f.append('</g>')
    # Main body, fur contour, pale chest and shoulder patch.
    f.append('<path d="M-110 -151Q-64 -202 25 -191Q111 -191 145 -139Q166 -103 137 -66Q92 -37 8 -48Q-77 -42 -119 -83Q-145 -118 -110 -151Z" fill="url(#foxFur)" stroke="#713b24" stroke-width="9" stroke-linejoin="round"/>')
    f.append('<path d="M12 -165Q71 -174 108 -138Q125 -111 100 -65Q68 -45 37 -58Q54 -91 12 -165Z" fill="#f7e7c9" stroke="#b87543" stroke-width="5"/>')
    f.append('<path d="M-82 -142Q-45 -177 -4 -164M-70 -91Q-17 -74 18 -98" fill="none" stroke="#f7b46d" stroke-width="5" opacity=".65" stroke-linecap="round"/>')
    # Berry satchel and woven basket: prop stays attached to Fox across the walk.
    f.append('<path d="M-95 -153Q-65 -110 -12 -105" fill="none" stroke="#563a2d" stroke-width="8"/>')
    f.append('<g transform="translate(-104 -103)"><path d="M-20 -24Q8 -37 37 -23L32 19Q3 35 -28 17Z" fill="#a66a3e" stroke="#593b2a" stroke-width="5"/><path d="M-27 -19Q5 -31 38 -17L36 -7Q6 6 -25 -7Z" fill="#d2a05d" stroke="#69452f" stroke-width="4"/><path d="M-18 -5L-12 21M0 -6L5 27M18 -7L22 21" stroke="#795033" stroke-width="3"/><circle cx="-7" cy="-27" r="10" fill="#b94440" stroke="#762e2b" stroke-width="3"/><circle cx="13" cy="-29" r="10" fill="#d24e43" stroke="#762e2b" stroke-width="3"/><path d="M-11 -39Q-3 -49 3 -40M8 -42Q16 -52 22 -42" stroke="#5d7b42" stroke-width="4" fill="none"/></g>')
    # Near hind leg.
    a = math.sin(phase + math.pi) * 22 * stride
    f.append(f'<g transform="translate(-63 -88) rotate({a:.2f})"><path d="M-14 -3Q-25 28 -16 66Q-10 83 3 80Q17 77 13 59L8 3Z" fill="url(#foxFur)" stroke="#743f28" stroke-width="6"/><path d="M-9 73Q-23 77 -22 89Q-16 99 8 97Q26 97 23 84Q17 73 6 72Z" fill="#c96d36" stroke="#743f28" stroke-width="5"/></g>')
    # Near front leg lifts and presses against the log, then returns to a planted stance.
    front_angle = mix(math.sin(phase) * 18 * stride, -48, paw_push)
    f.append(f'<g transform="translate(91 -87) rotate({front_angle:.2f})"><path d="M-13 -4Q-24 27 -15 62Q-10 78 4 79Q17 76 13 60L8 2Z" fill="url(#foxFur)" stroke="#743f28" stroke-width="6"/><path d="M-8 69Q-22 75 -22 88Q-16 99 8 97Q27 98 23 84Q17 72 7 71Z" fill="#c96d36" stroke="#743f28" stroke-width="5"/><path d="M-8 86L-4 92M6 86L10 92" stroke="#f6d1a5" stroke-width="3" stroke-linecap="round"/></g>')
    # Head + muzzle, with separate animated ears, pupils and mouth.
    f.append(f'<g transform="translate(108 -151) rotate({head_turn:.2f})">')
    f.append('<path d="M-49 -27Q-67 -63 -53 -105Q-47 -119 -28 -94L-15 -65Z" fill="#c96631" stroke="#743b27" stroke-width="7"/>')
    f.append('<path d="M-46 -41Q-52 -72 -48 -93Q-34 -72 -25 -56Z" fill="#efb1a0"/>')
    f.append('<path d="M43 -30Q65 -73 52 -112Q47 -124 28 -97L14 -64Z" fill="#c96631" stroke="#743b27" stroke-width="7"/>')
    f.append('<path d="M43 -43Q52 -79 47 -97Q34 -73 24 -56Z" fill="#efb1a0"/>')
    f.append('<path d="M-57 -38Q-57 -103 -9 -122Q42 -131 69 -85Q89 -47 61 -8Q39 21 -3 15Q-45 8 -57 -38Z" fill="url(#foxFur)" stroke="#713b24" stroke-width="8"/>')
    f.append('<path d="M-54 -32Q-30 -58 -4 -48Q20 -44 31 -18Q16 14 -12 18Q-43 10 -54 -32Z" fill="#f6e2c2" stroke="#b87543" stroke-width="4"/>')
    f.append('<path d="M27 -25Q54 -45 77 -31Q96 -17 82 1Q66 20 35 12Q14 8 7 -5Z" fill="#f5e4cb" stroke="#a85f3c" stroke-width="5"/>')
    f.append('<path d="M74 -26Q92 -34 100 -20Q103 -8 86 -4Q73 -6 74 -26Z" fill="#282026" stroke="#713b24" stroke-width="4"/>')
    # Brow, eye whites and pupils.
    f.append(f'<ellipse cx="23" cy="-48" rx="13" ry="{15*b:.2f}" fill="#fff7df"/>')
    f.append(f'<ellipse cx="27" cy="-46" rx="5.7" ry="{9*b:.2f}" fill="#24212a"/>')
    f.append('<path d="M9 -69Q24 -78 38 -68" stroke="#713b24" stroke-width="5" fill="none" stroke-linecap="round"/>')
    f.append('<circle cx="53" cy="-3" r="3.2" fill="#7d4d39"/><circle cx="63" cy="-8" r="2.5" fill="#7d4d39"/>')
    f.append('<path d="M36 8Q48 21 62 10" stroke="#75432f" stroke-width="4" fill="none" stroke-linecap="round"/>')
    mouth = 4 + 7 * (0.5 + 0.5 * math.sin(t * 11)) if scene in (3, 4) else 3
    f.append(f'<path d="M55 9Q68 {9+mouth} 78 6" stroke="#753a31" stroke-width="4" fill="none" stroke-linecap="round"/>')
    f.append('<path d="M-2 -100Q18 -124 48 -99" stroke="#f8b56d" stroke-width="5" fill="none" opacity=".65"/>')
    f.append('</g></g>')
    return "".join(f)


def turtle_svg(x: float, ground: float, t: float, scene: int, u: float) -> str:
    if scene <= 3:
        root_x = 1065
        walk = 0.12 if scene == 1 else 0.0
    elif scene == 4:
        root_x = mix(1065, 745, ease(u))
        walk = 1.0
    else:
        root_x = 745
        walk = 0.10
    phase = t * 8.4
    bob = abs(math.sin(phase)) * 3.2 * walk
    head_turn = -7 * ease(u) if scene == 2 else (5 if scene == 4 else 0)
    b = blink(t, 1.25)
    f = [f'<g id="olive" transform="translate({root_x:.2f} {ground+bob:.2f})">']
    f.append('<ellipse cx="0" cy="-2" rx="105" ry="15" fill="#10251f" opacity=".22" filter="url(#softShadow)"/>')
    for idx, lx in enumerate((-35, 40)):
        for side in (0, 1):
            angle = math.sin(phase + idx * math.pi + side * math.pi) * 18 * walk
            y = -58 if side == 0 else -70
            f.append(f'<g transform="translate({lx} {y}) rotate({angle:.2f})"><path d="M-12 -2Q-21 19 -13 38Q-8 50 6 47Q20 42 14 29L8 -2Z" fill="#74a55e" stroke="#355e42" stroke-width="5"/><path d="M-9 38Q2 31 13 40Q23 48 12 57Q-8 63 -18 52Q-20 44 -9 38Z" fill="#83b96b" stroke="#355e42" stroke-width="4"/><path d="M-5 48L-2 52M5 47L8 51" stroke="#d6e0a6" stroke-width="2.5"/></g>')
    f.append('<path d="M-67 -99Q-46 -128 17 -130Q77 -125 84 -90L64 -61Q12 -43 -53 -65Z" fill="#8b6d3d" stroke="#3b4c35" stroke-width="8"/>')
    f.append('<path d="M-86 -109Q-93 -164 -35 -187Q30 -210 85 -166Q111 -138 82 -98Q46 -66 -32 -77Q-75 -80 -86 -109Z" fill="url(#shell)" stroke="#364b35" stroke-width="9"/>')
    f.append('<path d="M-42 -177Q-7 -196 24 -183L40 -151L1 -128L-42 -145Z" fill="#9d8750" stroke="#526543" stroke-width="4"/>')
    f.append('<path d="M-79 -127Q-48 -155 -21 -140L-33 -104L-73 -103Z" fill="#9d8750" stroke="#526543" stroke-width="4"/>')
    f.append('<path d="M29 -177Q70 -175 85 -141L54 -112L21 -142Z" fill="#9d8750" stroke="#526543" stroke-width="4"/>')
    f.append('<path d="M-32 -105Q-2 -128 28 -104L54 -85Q13 -70 -34 -83Z" fill="#9d8750" stroke="#526543" stroke-width="4"/>')
    f.append('<path d="M-65 -117Q-36 -127 -22 -146M42 -171Q55 -150 68 -137M-20 -91L5 -83" fill="none" stroke="#d2b875" stroke-width="3" opacity=".7"/>')
    f.append(f'<g transform="translate(71 -126) rotate({head_turn:.2f})">')
    f.append('<path d="M-10 -16Q-31 -42 -12 -62Q8 -78 39 -57L55 -30Q70 -2 47 16Q15 32 -12 12Z" fill="#83b96b" stroke="#355e42" stroke-width="7"/>')
    f.append('<path d="M-10 -13Q6 -24 24 -13Q47 -1 57 -12Q49 20 20 23Q-6 17 -10 -13Z" fill="#b7ce87" opacity=".8"/>')
    f.append(f'<ellipse cx="29" cy="-43" rx="10" ry="{12*b:.2f}" fill="#fff8dc"/>')
    f.append(f'<ellipse cx="32" cy="-42" rx="4.6" ry="{7*b:.2f}" fill="#252a23"/>')
    f.append('<path d="M19 -59Q30 -68 41 -60" fill="none" stroke="#426744" stroke-width="4" stroke-linecap="round"/>')
    f.append('<ellipse cx="56" cy="-14" rx="4" ry="3" fill="#4d754b"/>')
    f.append('<path d="M34 6Q46 15 57 5" fill="none" stroke="#426744" stroke-width="3.5" stroke-linecap="round"/>')
    f.append('</g>')
    f.append('<path d="M-83 -87Q-111 -77 -121 -61Q-107 -54 -87 -68Z" fill="#75a65d" stroke="#355e42" stroke-width="4"/>')
    for sx, sy in [(-53,-92),(-27,-89),(1,-97),(43,-100)]:
        f.append(f'<circle cx="{sx}" cy="{sy}" r="4" fill="#c5d99c" opacity=".8"/>')
    f.append('</g>')
    return "".join(f)


def background_svg(t: float, scene: int, u: float) -> str:
    shift = 22 * math.sin(t * .23)
    water_shift = 38 * (t % 2.4) / 2.4
    fx = []
    fx.append('''<defs>
      <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#435b72"/><stop offset=".46" stop-color="#9cae9a"/><stop offset="1" stop-color="#e8bd87"/></linearGradient>
      <linearGradient id="farHills" x2="0" y2="1"><stop stop-color="#607d71"/><stop offset="1" stop-color="#395d52"/></linearGradient>
      <linearGradient id="ground" x2="0" y2="1"><stop stop-color="#74905d"/><stop offset="1" stop-color="#2e5142"/></linearGradient>
      <linearGradient id="water" x2="0" y2="1"><stop stop-color="#9bc6bb"/><stop offset=".4" stop-color="#4f9ba0"/><stop offset="1" stop-color="#2f6c79"/></linearGradient>
      <linearGradient id="foxFur" x2=".25" y2="1"><stop stop-color="#f7a34e"/><stop offset=".55" stop-color="#d66c32"/><stop offset="1" stop-color="#9f4829"/></linearGradient>
      <linearGradient id="shell" x2=".7" y2="1"><stop stop-color="#8b9560"/><stop offset=".45" stop-color="#586b45"/><stop offset="1" stop-color="#344d39"/></linearGradient>
      <linearGradient id="bark" x2="0" y2="1"><stop stop-color="#b88a58"/><stop offset=".5" stop-color="#855c3d"/><stop offset="1" stop-color="#573e30"/></linearGradient>
      <radialGradient id="sunGlow"><stop stop-color="#f8dca6" stop-opacity=".5"/><stop offset="1" stop-color="#f8dca6" stop-opacity="0"/></radialGradient>
      <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="7"/></filter>
      <filter id="leafShadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
    </defs>''')
    fx.append('<rect width="1280" height="720" fill="url(#sky)"/>')
    fx.append('<circle cx="1020" cy="168" r="170" fill="url(#sunGlow)"/><circle cx="1020" cy="168" r="48" fill="#f8d9a1" opacity=".82"/>')
    fx.append('<path d="M0 360Q170 260 330 350T665 320T990 345T1280 300V720H0Z" fill="url(#farHills)"/>')
    fx.append('<path d="M0 420Q210 335 410 395T785 380T1110 400T1280 370V720H0Z" fill="#4d735d" opacity=".9"/>')
    fx.append(f'<g transform="translate({shift:.2f} 0)" opacity=".88">')
    for i, (tx, ty, r) in enumerate([(42,385,94),(180,345,125),(345,376,98),(530,350,115),(690,365,105),(1080,370,120),(1220,355,102)]):
        col = ["#385f51", "#436b56", "#315746"][i % 3]
        fx.append(f'<path d="M{tx-18} {ty+130}Q{tx-26} {ty+12} {tx-8} {ty-55}L{tx+12} {ty-55}Q{tx+30} {ty+20} {tx+18} {ty+130}Z" fill="#614b39"/>')
        fx.append(f'<g fill="{col}" stroke="#2b5144" stroke-width="5"><ellipse cx="{tx}" cy="{ty-80}" rx="{r}" ry="{r*.75}"/><ellipse cx="{tx-r*.55}" cy="{ty-30}" rx="{r*.55}" ry="{r*.54}"/><ellipse cx="{tx+r*.55}" cy="{ty-34}" rx="{r*.58}" ry="{r*.55}"/></g>')
        fx.append(f'<path d="M{tx-r*.55} {ty-79}Q{tx-r*.1} {ty-133} {tx+r*.45} {ty-100}" fill="none" stroke="#91ae78" stroke-width="6" opacity=".5"/>')
    fx.append('</g>')
    fx.append('<path d="M0 0H110Q83 130 119 250Q139 360 88 485L0 525Z" fill="#4d3d31"/><path d="M18 0Q40 180 23 385M67 0Q51 210 84 450" stroke="#88664b" stroke-width="10" fill="none" opacity=".55"/>')
    fx.append('<path d="M0 86Q40 -15 150 14Q214 30 205 126Q166 178 75 161Q30 150 0 86Z" fill="#315843" stroke="#244a3b" stroke-width="8"/>')
    fx.append('<path d="M1280 0H1185Q1209 130 1178 255Q1154 354 1200 493L1280 520Z" fill="#4b3b30"/><path d="M1261 0Q1238 185 1250 412M1210 0Q1236 185 1202 420" stroke="#87654a" stroke-width="9" fill="none" opacity=".55"/>')
    fx.append('<path d="M1280 105Q1230 10 1130 35Q1060 57 1080 148Q1120 195 1206 170Z" fill="#2e5941" stroke="#244a3b" stroke-width="8"/>')
    fx.append('<path d="M0 444Q145 415 270 451T545 442Q655 430 700 460L720 720H0Z" fill="url(#ground)"/><path d="M990 445Q1100 418 1280 447V720H948Z" fill="#486e4b"/>')
    fx.append('<path d="M0 552Q220 500 430 552T720 545" stroke="#abc078" stroke-width="13" fill="none" opacity=".25"/>')
    fx.append('<path d="M660 463Q735 420 808 450Q894 482 1000 454Q1070 478 1100 554Q1014 611 928 584Q827 553 752 594Q687 577 642 533Z" fill="url(#water)" stroke="#335f57" stroke-width="12"/>')
    for k in range(8):
        x = 680 + k * 48 + (water_shift % 48)
        y = 500 + (k % 3) * 23 + 4 * math.sin(t * 2 + k)
        fx.append(f'<path d="M{x:.1f} {y:.1f}q18 -7 36 0q18 7 36 0" stroke="#c4e0ce" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/>')
    fx.append('<path d="M640 460Q715 408 802 444M970 448Q1060 420 1110 517" stroke="#afbb79" stroke-width="13" fill="none" stroke-linecap="round"/>')
    fx.append('<ellipse cx="760" cy="505" rx="57" ry="22" fill="#657966" stroke="#405744" stroke-width="7"/><path d="M730 501Q757 478 786 496" stroke="#a2ad8b" stroke-width="5" fill="none"/>')
    fx.append('<ellipse cx="1030" cy="498" rx="64" ry="24" fill="#75816b" stroke="#405744" stroke-width="7"/><path d="M991 496Q1024 474 1059 491" stroke="#b2b68c" stroke-width="5" fill="none"/>')
    log_progress = ease(u) if scene == 3 else (1.0 if scene >= 4 else 0.0)
    log_angle = mix(0, -3, log_progress)
    log_x = mix(1170, 835, log_progress)
    log_y = mix(467, 468, log_progress)
    fx.append(f'<g transform="translate({log_x:.2f} {log_y:.2f}) rotate({log_angle:.2f})">')
    fx.append('<path d="M-188 -5Q-168 -35 -128 -25L143 -29Q182 -18 192 5Q174 34 131 27L-151 26Q-183 22 -188 -5Z" fill="url(#bark)" stroke="#543b2e" stroke-width="8"/>')
    fx.append('<path d="M-152 -7Q-80 -21 0 -10T155 -8M-160 13Q-75 1 12 13T162 12" fill="none" stroke="#d0a06b" stroke-width="5" opacity=".55"/>')
    fx.append('<ellipse cx="-175" cy="0" rx="19" ry="27" fill="#9a714a" stroke="#543b2e" stroke-width="6"/><ellipse cx="-175" cy="0" rx="10" ry="17" fill="none" stroke="#d2a475" stroke-width="4"/>')
    fx.append('<path d="M-75 -25Q-60 -57 -42 -51Q-23 -40 -30 -24M88 23Q109 47 125 31" stroke="#6c4a32" stroke-width="7" fill="none" stroke-linecap="round"/>')
    fx.append('</g>')
    fx.append('<g stroke-linecap="round">')
    for i in range(38):
        x = (i * 79 + 21) % 1280
        y = 585 + (i % 4) * 23
        h = 24 + (i % 5) * 7
        fx.append(f'<path d="M{x} {y}q{-12+(i%3)*6} {-h*.55} {-18+(i%4)*11} {-h}" fill="none" stroke="{["#9db36e","#75965e","#b4b978"][i%3]}" stroke-width="5"/>')
    fx.append('</g>')
    for x, y, s in [(120,596,1),(595,608,.75),(1138,590,.9),(1215,640,.65)]:
        fx.append(f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0V24" stroke="#d5d0ae" stroke-width="5"/><path d="M-16 3Q-12 -20 0 -14Q13 -25 17 3Q0 12 -16 3Z" fill="#d66c67" stroke="#78443e" stroke-width="4"/><path d="M-8 -3L-3 -7M7 -1L10 -6" stroke="#fff1d7" stroke-width="4"/></g>')
    for k in range(8):
        x = (130 + k * 151 + 22 * math.sin(t * 1.2 + k)) % 1230
        y = 300 + (k % 3) * 52 + 16 * math.sin(t * 1.7 + k)
        op = .25 + .35 * (.5 + .5 * math.sin(t * 3 + k))
        fx.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#ffe9a8" opacity="{op:.2f}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#ffe9a8" opacity=".08"/>')
    return "".join(fx)


def camera_view(scene: int, u: float, t: float) -> tuple[float, float, float, float]:
    centers = [570, 650, 835, 850, 865, 680]
    widths = [1280, 1180, 1110, 1100, 1100, 1280]
    prev = scene - 1 if scene > 0 else 0
    target_width = widths[scene]
    target_center = centers[scene]
    if scene > 0:
        start_width, start_center = widths[prev], centers[prev]
    else:
        start_width, start_center = widths[0], centers[0]
    k = ease(u)
    vw = mix(start_width, target_width, k)
    center = mix(start_center, target_center, k) + 12 * math.sin(u * math.pi)
    vh = vw * H / W
    vx = clamp(center - vw / 2, 0, W - vw)
    vy = (H - vh) / 2
    vy = clamp(vy + 5 * math.sin(t * .32), 0, H - vh)
    return vx, vy, vw, vh


def svg_frame(t: float, scene: int, u: float, durations: list[float]) -> bytes:
    caption = html.escape(STORY[scene]["caption"])
    vx, vy, vw, vh = camera_view(scene, u, t)
    fox = fox_svg(0, 529, t, scene, u)
    turtle = turtle_svg(0, 507 if scene <= 3 else 492, t, scene, u)
    paw_glow = ease(u) if scene == 3 else (1 - ease(u)) if scene == 4 else 0
    head_rays = "" if scene != 1 else '<g stroke="#f7df9f" stroke-width="4" stroke-linecap="round" opacity=".8"><path d="M545 293l-14 -13M559 278l-4 -18M579 285l8 -16"/></g>'
    title = STORY[scene]["title"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">
    {background_svg(t, scene, u)}
    {head_rays}
    <g transform="translate(0 0)">
      {fox}
      {turtle}
    </g>
    <g opacity="{paw_glow:.2f}" fill="none" stroke="#ffdfa1" stroke-width="7" stroke-linecap="round"><path d="M715 391q20 -24 44 -9M726 421q26 -18 49 -3"/></g>
    <rect x="34" y="34" width="395" height="42" rx="10" fill="#162a2a" opacity=".84"/>
    <text x="55" y="62" font-family="DejaVu Sans" font-size="19" font-weight="bold" letter-spacing="2" fill="#f8e4bd">WISE-LAB  •  WILD TALES</text>
    <rect x="34" y="625" width="1212" height="64" rx="13" fill="#142c2a" opacity=".93" stroke="#ddc99d" stroke-width="2"/>
    <text x="640" y="652" text-anchor="middle" font-family="DejaVu Sans" font-size="16" font-weight="bold" letter-spacing="2" fill="#b5c99d">{html.escape(title)}</text>
    <text x="640" y="678" text-anchor="middle" font-family="DejaVu Sans" font-size="25" font-weight="bold" fill="#fff6df" textLength="1110" lengthAdjust="spacingAndGlyphs">{caption}</text>
    <rect x="34" y="34" width="5" height="42" rx="2" fill="#e7a55c"/>
    </svg>'''.encode("utf-8")


def render() -> dict:
    durations, total = make_narration()
    make_ambience(total)
    starts: list[float] = []
    cur = 0.0
    for duration in durations:
        starts.append(cur)
        cur += duration
    frame_count = math.ceil(total * FPS)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required.")
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
        "-i", str(NARRATION), "-i", str(AMBIENCE),
        "-filter_complex", f"[1:a]volume=1.0[voice];[2:a]volume=0.18[bed];[voice][bed]amix=inputs=2:duration=first:normalize=0,apad,atrim=0:{total:.4f},afade=t=out:st={max(0,total-1.2):.4f}:d=1.2[a]",
        "-vf", f"fps={OUTPUT_FPS}",
        "-map", "0:v:0", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(OUTPUT_FPS), "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.4f}",
        "-movflags", "+faststart", str(MP4)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    last_scene = -1
    try:
        for frame in range(frame_count):
            t = min(total - 1 / FPS, frame / FPS)
            scene = max(i for i, start in enumerate(starts) if start <= t)
            local = t - starts[scene]
            duration = durations[scene]
            spoken_duration = duration - (0.18 if scene < len(STORY) - 1 else 0.0)
            u = clamp(local / max(.1, spoken_duration))
            svg = svg_frame(t, scene, u, durations)
            png = cairosvg.svg2png(bytestring=svg, output_width=W, output_height=H)
            with Image.open(BytesIO(png)) as im:
                raw = im.convert("RGB").tobytes()
            proc.stdin.write(raw)
            if frame % (FPS * 3) == 0 or scene != last_scene:
                print(f"RENDER {frame+1}/{frame_count}  scene {scene+1}/{len(STORY)}  t={t:.1f}s", flush=True)
            last_scene = scene
        proc.stdin.close()
        err = proc.stderr.read() if proc.stderr else b""
        code = proc.wait()
        if code != 0:
            raise RuntimeError(f"FFmpeg failed ({code}): {err.decode('utf-8', 'replace')[-4000:]}")
    except Exception:
        if proc.poll() is None:
            proc.kill()
        proc.wait()
        raise
    subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(MP4),
                    "-vf", "fps=0.5,scale=480:-1,tile=4x3", "-frames:v", "1", str(CONTACT)], check=True)
    report = {
        "engine": "WISE-LAB illustrated animal cutout + 2.5D camera",
        "story": "Finn the fox and Olive the turtle build a bridge across a forest stream",
        "characters": ["Finn the fox", "Olive the turtle"],
        "resolution": f"{W}x{H}", "fps": OUTPUT_FPS, "render_source_fps": FPS, "duration_seconds": round(total, 3),
        "rendered_source_frames": frame_count, "frames": int(round(total * OUTPUT_FPS)), "scenes": len(STORY), "camera_track": "six continuous pan/zoom beats",
        "animation": ["quadruped walk cycles", "tail swish", "ear twitch", "blinks", "head turns", "paw/log interaction", "turtle crossing", "moving stream and fireflies"],
        "audio": "offline English narration + procedural forest ambience and effects",
        "subtitle_file": str(SRT), "mp4": str(MP4),
    }
    with wave.open(str(NARRATION), "rb") as wf:
        report["narration_seconds"] = round(wf.getnframes() / wf.getframerate(), 3)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("DONE", json.dumps(report), flush=True)
    return report


if __name__ == "__main__":
    render()
