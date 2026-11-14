# WISE-LAB Animation Integration Lab

Isolated integration branch for the 14 November animation prototypes. Production-channel code and upload workflows are not modified.

## What is included

- `experiments/2026-11-14/`: original HTML, Pillow, Blender, rig and comic prototypes, preserved for comparison.
- `renderer/verify_render.py`: validates the MP4 container, audio/video streams, 1280×720 dimensions and expected duration.
- `.github/workflows/animation-benchmark.yml`: compiles every Python prototype, renders a 20-second sample using the production-character benchmark, validates the MP4 and uploads it as an artifact.
- Duplicate upload `2d_rig_benchmark(1).py` was byte-identical to `2d_rig_benchmark.py`; only one copy is retained.

## Run locally

Install Python Pillow, FFmpeg and eSpeak NG, then run:

```bash
python -m pip install Pillow
python experiments/2026-11-14/production_character_benchmark.py
python renderer/verify_render.py renders/wise-lab-production-character-20sec.mp4
```

## Current limitations

This is an integration smoke-test, not the finished long-form scene engine. The Blender pass remains a separate experiment and is not yet composited into this render. Narration is currently generated as one continuous track; word-level timing, per-scene sound design, full 2D/3D compositing, vertical export, and a generalized script-to-scene planner remain follow-up work. Captions in the benchmark are burned in once by the renderer to avoid duplicate subtitle ownership.

## CI output

The workflow uploads `wise-lab-production-character-20sec.mp4` and `ffprobe-report.json` as a GitHub Actions artifact.
