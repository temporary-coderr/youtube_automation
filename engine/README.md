# Cinematic Engine — Development Notes

This branch is an isolated engineering track. The production WISE-LAB repository is not modified.

## Current milestone: deterministic preview renderer

The first renderer uses the existing layered SVG motion study at `prototype/index.html`:

1. Chromium opens the authored scene.
2. Python calls `window.renderAt(t)` at exact timestamps.
3. Playwright captures one PNG per frame.
4. FFmpeg encodes H.264 MP4.
5. ffprobe validates codec, dimensions, duration, and file size.
6. A JSON QA report is saved beside the MP4.

No AI API or voice service is required for this test. Audio can be supplied with `--audio path/to/file.wav`.

## Run locally

Install FFmpeg, then:

```bash
python -m pip install -r requirements.txt
playwright install chromium
python engine/render_prototype.py --duration 12 --fps 24 --width 1280 --height 720
```

Portrait preview uses a character-centered crop rather than stretching the landscape artwork:

```bash
python engine/render_prototype.py --duration 12 --fps 24 --width 720 --height 1280 --output renders/portrait-preview.mp4
```

## GitHub Actions

Open **Actions → Cinematic Engine Preview → Run workflow** on branch `feature/cinematic-engine`. The workflow uploads the MP4 and QA report as an artifact.

## Quality gates before production

A successful encode is only a technical pass, not proof of cinematic quality. Every milestone must also be reviewed for:

- connected anatomy and clean joint pivots throughout the full motion;
- readable character scale and composition;
- visible motion in the character, props, environment, and camera;
- no clipping, layer collisions, or sudden transform jumps;
- one caption owner and correct narration synchronization;
- deliberate scene transitions and consistent color / lighting;
- both landscape and portrait composition.

## Planned architecture

- **Scene planner:** convert script beats into a timed, validated JSON scene plan.
- **Character rig:** reusable skeleton with shoulder, elbow, wrist, hip, knee, and foot pivots.
- **Motion system:** reusable walk, reach, turn, gesture, idle, and prop-interaction actions.
- **Environment system:** reusable layered SVG sets with foreground / midground / background parallax.
- **Camera system:** deterministic pans, pushes, tracking, reframing, and transitions.
- **Audio timeline:** narration, music, and sound effects with ducking and per-scene timing.
- **Visual QA:** frame sampling, contact sheets, bounds checks, and human review before promotion.

AI may help interpret a script or propose scene direction, but the renderer must have deterministic defaults and must not depend on an API being available.
