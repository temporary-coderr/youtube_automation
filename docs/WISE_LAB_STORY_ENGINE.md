# WISE-LAB Script-Directed Animation Engine

## Ownership and production boundary

The creator supplies the complete original script in `scripts/narration.txt`. That file is the source of truth for hooks, story, dialogue, research claims, wording and narration order.

The visual director may interpret the script and choose scenes, characters, actions, environments, props, stickers, camera moves and transitions. It must never write, rewrite, paraphrase, add or remove spoken content. Narration generation continues to read the creator's original file.

## Fixed recurring cast

The reusable cast bible is `src/wiseLabCast.js`:

| ID | Audience-facing name | Role / rig profile |
|---|---|---|
| `alex` | Alex | Main young-adult lead |
| `maya` | Maya | Friend / contrasting perspective |
| `ethan` | Ethan | Friend / challenger |
| `zoe` | Zoe | Grounded perspective |
| `oliver` | Oliver | Child perspective |
| `arthur` | Arthur | Elder perspective |

The engine selects only the cast required by the story: 2–7 distinct characters per video, no more than 2 in one scene. Character identity, palette and scale are stored centrally. A new recurring character must be designed and rigged before being admitted to the library; one-off characters are not generated for every episode.

## Visual direction pipeline

1. Creator writes or replaces `scripts/narration.txt`.
2. `scripts/plan_scenes.py` splits the script for planning only. It does not write to the narration file.
3. If `GEMINI_API_KEY` is available, Gemini is asked for visual direction only, constrained to the cast, environments, actions, props and sticker vocabulary. Invalid or unavailable AI output falls back to deterministic planning.
4. The planner writes `src/generatedScenePlan.js` immediately before rendering. Scene durations are estimated from the supplied script length.
5. `src/sceneDirector.js` and `src/storyRules.js` reject unknown assets, invalid stickers, invalid cast IDs, and cast-count violations.
6. Remotion renders the generated scene sequence using the existing articulated character rig, scene environments, camera motion, sticker layer, vector props, narration and ambience.

## Reusable asset library

- `src/wiseLabAssets.js`: runtime catalogue for fixed characters, supported environments, props, motion vocabulary, stickers, camera moves and transitions.
- `assets/item-library.json`: machine-readable asset manifest.
- `src/ScenePropLayer.jsx`: reusable vector props with lightweight motion and hand-aware phone placement.
- `src/StoryStickerLayer.jsx`: tag, stat, definition, steps, quote, compare, diagram, timeline and callout overlays.
- `src/WiseLabFilm.jsx` and `src/EnvironmentLibrary.jsx`: Remotion character rig, layered cafe/street/bedroom/park scenes plus office/classroom/library/living-room vector sets, camera moves and scene renderer.

## Production and monetization safeguards

- Reuse rigs and individual assets for efficiency; do not reuse entire video sequences as a substitute for original storytelling.
- A consistent narrator and recurring cast are brand identity, not a reason to vary voices artificially.
- Every episode must still have a distinct creator-written script and story progression.
- The visual plan is checked before render; it cannot silently change the creator's story.
- Review rendered videos for scene accuracy, object/character interactions, readability, pacing, captions, audio and visual repetition before upload.

## Current implementation boundary

This branch establishes the six-profile cast registry, cast-count validation, visual asset manifest, optional AI visual planning with deterministic fallback, variable scene timing, reusable prop rendering and expanded sticker vocabulary. The existing hand-authored demo scenes remain as a local fallback if the planner has not run. New environment artwork, richer per-character rig geometry and additional interaction clips should be added incrementally and verified in rendered previews rather than represented as finished when they are not.
