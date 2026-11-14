#!/usr/bin/env python3
"""Validate the asset-first WISE-LAB 2D cutout story contract."""
import argparse, json, sys
from pathlib import Path

REQUIRED = {"head","hair_back","hair_front","torso","upper_arm_L","forearm_L","hand_L","upper_arm_R","forearm_R","hand_R","pelvis","thigh_L","shin_L","foot_L","thigh_R","shin_R","foot_R"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    args = ap.parse_args()
    data = json.loads(args.project.read_text(encoding="utf-8"))
    root = args.project.parent
    for key in ("title","fps","canvas","narration","characters","scenes"):
        if key not in data: raise ValueError(f"missing project field: {key}")
    if data["fps"] not in (24,25,30): raise ValueError("fps must be 24, 25 or 30")
    canvas = data["canvas"]
    if canvas.get("aspect") not in ("16:9","9:16") or min(canvas.get("width",0),canvas.get("height",0)) < 720:
        raise ValueError("canvas must be HD and use 16:9 or 9:16")
    if not (root / data["narration"]).is_file(): raise ValueError("narration file not found")
    ids = set()
    for ref in data["characters"]:
        cid = ref["id"]
        if cid in ids: raise ValueError(f"duplicate character id: {cid}")
        ids.add(cid)
        base = root / "assets" / "characters" / cid
        manifest = json.loads((base / "character.json").read_text(encoding="utf-8"))
        missing = REQUIRED - set(manifest.get("layers", []))
        if missing: raise ValueError(f"{cid} missing layers: {sorted(missing)}")
        for rel in (manifest["model_sheet"], manifest["rig_file"]):
            if not (base / rel).is_file(): raise ValueError(f"{cid} missing asset: {rel}")
        for layer in REQUIRED:
            if not (base / "layers" / f"{layer}.png").is_file():
                raise ValueError(f"{cid} missing transparent layer: {layer}.png")
    cursor = 0.0
    for n, scene in enumerate(data["scenes"], 1):
        start, end = float(scene["start"]), float(scene["end"])
        if start < 0 or end <= start: raise ValueError(f"scene {n}: invalid time range")
        if abs(start-cursor) > .02: raise ValueError(f"scene {n}: timeline gap/overlap at {cursor:.2f}s")
        if not scene.get("environment") or not scene.get("actions") or not scene.get("camera"):
            raise ValueError(f"scene {n}: environment, actions and camera keys are required")
        if set(scene.get("characters",[])) - ids: raise ValueError(f"scene {n}: unknown character")
        cursor = end
    expected = float(data.get("duration_seconds", cursor))
    if abs(cursor-expected) > .05: raise ValueError(f"timeline ends at {cursor:.2f}s, expected {expected:.2f}s")
    print(json.dumps({"status":"manifest_valid","title":data["title"],"scene_count":len(data["scenes"]),"duration_seconds":cursor,"characters":sorted(ids),"canvas":canvas},indent=2))

if __name__ == "__main__":
    try: main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
