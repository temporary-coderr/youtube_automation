# Mixamo action-library experiment

This is isolated. It does not replace or edit the existing hybrid Blender engine or comic engine.

## Download a matching Mixamo set

Use a free Adobe ID at https://www.mixamo.com/ and select one humanoid character. Download:
- character.fbx: the chosen character, With Skin, preferably T-pose.
- One FBX per action in actions/, e.g. walk_in_place.fbx, sit_down.fbx, typing.fbx, reach.fbx, idle.fbx.
- Download every action using the same character/rig. For action FBXs choose Without Skin to reduce file size.
- For walk cycles choose In Place for the first test so root motion does not drift the character out of frame.

Place files locally:
assets/mixamo/character.fbx
assets/mixamo/actions/walk_in_place.fbx
assets/mixamo/actions/sit_down.fbx
assets/mixamo/actions/typing.fbx
assets/mixamo/actions/reach.fbx
assets/mixamo/actions/idle.fbx

## Keep raw Mixamo files private

Raw FBX files are excluded from Git by the root .gitignore. Do not upload them to a public repository or redistribute them as standalone assets. Adobe's Mixamo FAQ says its characters and animations can be used royalty-free in personal and commercial projects: https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html

## Run

blender -b --python prototype/mixamo_action_library.py -- --self-test
blender -b --python prototype/mixamo_action_library.py

The self-test validates Blender action creation/assignment without external files. The full importer reads the character and animation FBXs, checks matching bone names, binds each action to the base rig, and saves a .blend library plus JSON report under renders/mixamo-library/.

## Integration gate

Do not replace the procedural hybrid character yet. First inspect character style and side/three-quarter readability, action binding, foot sliding, prop interaction compatibility, and render time per second of finished video. Only after the preview passes should we build a bridge into the hybrid compositor. The comic engine remains untouched as the faster fallback.
