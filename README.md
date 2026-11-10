# WISE-LAB Animation Lab

An isolated sandbox for testing a new animation direction without changing the production repository.

## Experiment direction

**Cinematic 2D motion storytelling**: large readable characters, layered environments, camera movement, object animation, smooth transitions, and narration-synchronized captions.

## Non-negotiable test rules

- This repository is experimental; production code in `USA-channel` is untouched.
- No stock footage or raster scene backgrounds in the target style.
- Landscape (16:9) and vertical (9:16) output must both remain supported.
- Character scale and composition must be deliberate; the lead should be clearly readable.
- Every scene needs visible motion beyond a static image or simple fade.
- Captions must have a single rendering owner to prevent duplicate subtitles.
- Keep rendering lightweight enough for GitHub Actions.

## First milestone

Build a short 30–45 second sample and inspect the rendered MP4 before integrating anything into production.

## Planned pipeline

1. Script beats -> scene timeline.
2. Scene timeline -> layered vector scene descriptions.
3. Timeline -> camera, character, prop, and transition keyframes.
4. Render frames -> encode MP4.
5. Mix narration, sound effects, and one caption track.

The initial prototype will favor a small deterministic renderer over a heavyweight animation framework.