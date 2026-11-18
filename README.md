# WISE-LAB Animation Engine

WISE-LAB is a script-first 2D animation production system. The creator supplies the original script in `scripts/narration.txt`; the engine creates the visual direction and production around it.

## Core principles

- Creator-owned hooks, stories, dialogue, claims and narration remain unchanged.
- A fixed recurring cast is reused across videos: Alex, Maya, Ethan, Zoe, Oliver and Arthur.
- Each video uses only the 2–7 characters its story needs.
- Visual direction may be AI-assisted, but AI is restricted to scenes, actions, environments, props, camera direction and explanatory graphics.
- Reusable vector rigs, props and stickers improve consistency and production efficiency.
- No stock footage is used in the target visual style.
- Narration timing drives the in-video caption track and scene timeline.

## Production workflow

1. Put the creator-written script in `scripts/narration.txt`.
2. Run `python scripts/plan_scenes.py` to produce a visual-only scene plan. Gemini is optional; a deterministic planner is available as fallback.
3. Run `python scripts/generate_narration.py` to generate audio, SRT and timed caption data.
4. Run the Remotion composition to render the film.
5. Review the rendered MP4 for visual accuracy, motion, pacing, caption sync, sound and originality before upload.

## Main modules

- `src/wiseLabCast.js` — recurring character bible and cast constraints.
- `src/wiseLabAssets.js` / `assets/item-library.json` — reusable visual asset catalogue.
- `src/sceneDirector.js` / `scripts/plan_scenes.py` — visual planning and validation.
- `src/WiseLabFilm.jsx` — character rig, environments, camera and Remotion scene composition.
- `src/ScenePropLayer.jsx` — reusable vector props.
- `src/StoryStickerLayer.jsx` — animated explanatory graphics.
- `src/NarrationCaptionLayer.jsx` — single narration-synchronized subtitle track.

See [docs/WISE_LAB_STORY_ENGINE.md](docs/WISE_LAB_STORY_ENGINE.md) for the architecture and current implementation boundaries.
