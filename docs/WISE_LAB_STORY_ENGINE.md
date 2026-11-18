# WISE-LAB Small-Cast Story Engine

## The creative change

The engine is moving away from generating a new character or bespoke animation for every narration line. WISE-LAB stories will use a small recurring cast. The characters carry the human story; motion stickers, labels, diagrams and kinetic typography carry supporting explanations.

## Recurring cast

| ID | Role | Visual identity |
|---|---|---|
| `arjun` | Main relatable lead | Dark slate hoodie, dark trousers, messy dark hair |
| `maya` | Friend / contrasting perspective | Warm ochre top, dark trousers, soft-wave hair |
| `kabir` | Friend / challenger | Teal top, charcoal trousers, short-curl silhouette |
| `zoya` | Friend / grounded voice | Muted violet top, deep trousers, curly-bob silhouette |

The cast bible lives in `src/wiseLabCast.js`. Do not create one-off characters for examples, statistics or metaphors.

## Scene design rules

1. A story is built around one lead and, when needed, one or two recurring supporting characters.
2. Prefer two characters or fewer in a scene; the validator currently caps a scene at three.
3. Use a new character only when the story needs a new relationship role. Add them to the cast bible first.
4. Keep the character design stable. Vary pose, gesture, staging, camera, props, lighting and environment—not identity.
5. Do not literalize every narration sentence into a new animated object.
6. Supporting knowledge belongs in overlays: concept cards, definition stickers, stat callouts, comparison cards, three-step takeaways, speech bubbles and highlighted keywords.
7. Keep one main story action per shot. A sticker should clarify the idea, not compete with the character.
8. Captions remain the single narration-synchronized subtitle track. Stickers are supplemental editorial graphics, not duplicate captions.

## Sticker vocabulary

Implemented in `src/StoryStickerLayer.jsx`:

- `tag`: short chapter/idea label
- `stat`: one number or short evidence callout
- `definition`: psychology term and plain-language explanation
- `steps`: up to three practical steps
- `quote`: memorable takeaway
- `compare`: two-column contrast

Each scene can optionally provide a `sticker` object. Keep text concise; detailed evidence and citations should be in narration or the description, not a wall of tiny on-screen text.

## Current implementation

- `src/wiseLabCast.js`: stable cast bible and cast constraints.
- `src/storyRules.js`: scene validator that rejects unknown cast IDs and unsupported sticker types.
- `src/StoryStickerLayer.jsx`: reusable animated information overlays.
- `src/WiseLabFilm.jsx`: existing Remotion story now uses the cast registry and includes five sample sticker beats.

This is a controlled first integration. It deliberately keeps the current renderer, backgrounds, camera moves, character rigs, narration and audio path intact while changing how stories are authored and how supporting information is presented.
