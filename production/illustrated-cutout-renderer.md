# WISE-LAB Illustrated Cutout Renderer

This is an asset-first path: Blender imports painted PNG layers from an OpenRaster (.ora) project, binds the layers to named armature bones, animates the rig, renders frames and encodes an MP4.

## What changes
- Character appearance comes from painted artwork, not code-drawn circles, capsules or procedural human bodies.
- Hair, head, torso, clothing, arms, hands, legs and feet remain separate transparent layers.
- Each animated layer is attached to a named bone. Layer pivots are checked against the bone head.
- Missing artwork or rig layers fail loudly. There is no silent primitive fallback.
- Extra environment artwork can remain unrigged as additional layers.
- Landscape and vertical output are supported.

## Artwork prerequisite
The repository currently has a rig-map example but **does not yet contain an approved layered character artwork file**. Add an authored .ora at assets/characters/wise-lab-main/character-scene.ora. It must use the layer names in prototype/illustrated_2d/rig-map.example.json and match its 1920x1080 canvas. Adjust the example rig pivots to the actual artwork before publishing.

Prepare the artwork in Krita or another layered illustration editor. Export as OpenRaster with transparent, overlapping limb segments at joints. A flattened PNG is not sufficient.

## Run
\`\`\`bash
blender --background --python production/ora_cutout_renderer.py -- \\
  --ora assets/characters/wise-lab-main/character-scene.ora \\
  --rig prototype/illustrated_2d/rig-map.example.json \\
  --out renders/preview.mp4 --duration 10 --fps 24 --width 1280 --height 720
\`\`\`

Or run **Illustrated 2D Cutout Preview** from GitHub Actions and supply the .ora and rig-map paths.

## Acceptance gate
A green workflow is only a technical pass. Inspect the actual MP4 and contact sheet for layer order, joint gaps, pivots, character scale, scene detail and framing. This first renderer establishes painted-art import and skeletal deformation; it is not yet a complete story editor, prop-constraint system, dialogue lip-sync or finished long-form pipeline.
