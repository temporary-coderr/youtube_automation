# Cinematic Engine — Development Notes

This is an isolated engineering track. The production WISE-LAB repository is not modified.

## Current milestone: deterministic skeletal-motion benchmark

The active preview is `prototype/animation-benchmark.html`. It uses a deterministic Canvas renderer with:
- two-bone inverse-kinematics calculations for elbows and knees;
- connected limb strokes with overlapping joint caps;
- a repeatable walk cycle and arm counter-swing;
- a reach / phone pickup / carry sequence;
- three timed environments, camera push/pan, rain, lighting and scene fades.

Python + Playwright call `window.renderAt(t)` at exact timestamps. FFmpeg encodes the captured frames to H.264 and ffprobe validates the output. The GitHub Actions workflow pins Ubuntu 24.04 to avoid the Playwright / Ubuntu 26.04 incompatibility.

## Run locally

Install FFmpeg and the Python requirements, then:

```bash
python -m pip install -r requirements.txt
playwright install chromium
python engine/render_prototype.py --html prototype/animation-benchmark.html --duration 12 --fps 24 --width 1280 --height 720
```

The preview workflow uploads the MP4, ffprobe report and a contact sheet as one artifact.

## Current quality status

This is an animation benchmark, not a finished character-animation product. The current art is deliberately simple so motion defects are easy to see. Known limitations:
- body mechanics during the pickup still need refinement (torso lean, weight shift, hand-to-prop contact);
- face, hands, clothing folds and silhouette are placeholder-quality vector shapes;
- the three scenes are timed studies, not yet a general JSON-driven scene system;
- no production narration / sound-effect timeline is connected yet.

Do not promote this benchmark to the production channel based on a successful encode. Review the MP4 and contact sheet first.

## Next engineering gates

1. Improve pickup mechanics: crouch, weight transfer, shoulder / elbow constraints, wrist orientation and prop attachment.
2. Add foot planting and stride phase so feet do not slide during walk cycles.
3. Replace the placeholder silhouette with a reusable rig definition and adjustable character proportions.
4. Add JSON scene timelines, camera tracks, reusable action clips and prop interaction anchors.
5. Add audio timeline, captions and automated visual checks (joint continuity, foot sliding, frame bounds and scene-transition coverage).
6. Validate both landscape and portrait crops before production integration.

AI can propose shot plans, but deterministic rendering and fallback behavior must work without an external API.
