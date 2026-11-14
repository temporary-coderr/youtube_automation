# WISE-LAB 2D Cutout Production Pipeline

This is an asset-first pipeline, not another procedural-character demo. Existing Blender hybrid, comic engine, 60-second pilot and rejected rigged-character experiment remain untouched.

## Production stack
- **Artwork:** original layered character illustrations on transparent PNGs, created from an approved model sheet. No code-drawn human bodies.
- **Rigging:** Blender armature with IK controls for shoulders, elbows, wrists, hips, knees and ankles. Artwork layers overlap at joints to prevent gaps.
- **Scene assembly:** separate Blender collections for character, props, foreground, midground, background, atmosphere and lighting. Camera and parallax are independent tracks.
- **Editorial:** narration is the timing master. Scene beats, actions, SFX and one caption track share its timeline.
- **Delivery:** FFmpeg H.264/AAC, 16:9 or 9:16, plus MP4, contact sheet, timing report and source .blend.

## Mandatory gates
1. **Design:** approve front, three-quarter and side views before rigging.
2. **Layer preparation:** head, hair, torso, upper/lower arms, hands, pelvis, upper/lower legs and feet must be separate transparent layers. Hands and props remain independently animatable.
3. **Rig:** build and inspect IK, pivots, parent/weight mapping and extreme bends in a neutral test.
4. **Motion test:** 8–12 seconds proving walk, stop, reach, grasp/release, turn and sit/stand. Reject distorted anatomy and floating contacts.
5. **Scene:** distinct environment, foreground/midground/background parallax, camera move, prop animation and transition.
6. **Editorial:** narration drives timing; exactly one caption renderer; SFX mixed under dialogue; no clipped audio.
7. **Release:** inspect the actual MP4 and contact sheet. Technical success never equals visual approval.

## Asset contract
Each character lives in `assets/characters/<id>/` and contains `character.json`, `model-sheet.png`, `layers/*.png`, and an approved `rig.blend`. Required semantic layers: head, hair_back, hair_front, torso, upper_arm_L, forearm_L, hand_L, upper_arm_R, forearm_R, hand_R, pelvis, thigh_L, shin_L, foot_L, thigh_R, shin_R, foot_R.

A story project JSON declares canvas, fps, narration, characters and scene beats. Each scene declares contiguous start/end times, environment, character actions and camera keys. `prototype/validate_cutout_project.py` enforces the asset and timeline contract before rendering.

## First milestone
Build and approve one illustrated character and reusable Blender rig. Then render a 10-second motion test. Do not build a full 60-second video or integrate this into production until the rig passes visual review.
