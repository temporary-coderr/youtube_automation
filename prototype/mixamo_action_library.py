#!/usr/bin/env python3
"""Isolated WISE-LAB Mixamo FBX action-library importer."""
import bpy, os, sys, json, glob, math

ROOT=os.path.abspath(".")
ASSET_DIR=os.path.join(ROOT,"assets","mixamo")
ACTION_DIR=os.path.join(ASSET_DIR,"actions")
OUT_DIR=os.path.join(ROOT,"renders","mixamo-library")
os.makedirs(OUT_DIR,exist_ok=True)

def cli_args():
    return sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def armatures(objects=None):
    objects=objects if objects is not None else bpy.context.scene.objects
    return [o for o in objects if o.type=="ARMATURE"]

def frame_range(action):
    return [int(math.floor(action.frame_range[0])),int(math.ceil(action.frame_range[1]))]

def import_fbx(path,use_anim=True):
    before=set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path,use_anim=use_anim,ignore_leaf_bones=True,
        automatic_bone_orientation=False,use_custom_normals=True,use_image_search=True)
    return list(set(bpy.data.objects)-before)

def remove_objects(objects):
    for obj in list(objects):
        if obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj,do_unlink=True)

def self_test():
    clear_scene()
    data=bpy.data.armatures.new("SmokeTestRigData")
    rig=bpy.data.objects.new("SmokeTestRig",data)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active=rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    root=data.edit_bones.new("mixamorig:Hips"); root.head=(0,0,0); root.tail=(0,0,.5)
    spine=data.edit_bones.new("mixamorig:Spine"); spine.head=root.tail; spine.tail=(0,0,1); spine.parent=root
    bpy.ops.object.mode_set(mode="POSE")
    bone=rig.pose.bones["mixamorig:Spine"]; bone.rotation_mode="XYZ"
    bone.rotation_euler[0]=0; bone.keyframe_insert(data_path="rotation_euler",frame=1)
    bone.rotation_euler[0]=.25; bone.keyframe_insert(data_path="rotation_euler",frame=12)
    bpy.ops.object.mode_set(mode="OBJECT")
    act=rig.animation_data.action; act.name="SELFTEST_Reach"; act.use_fake_user=True
    assert frame_range(act)==[1,12],frame_range(act)
    assert rig.animation_data.action==act
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR,"mixamo-library-selftest.blend"))
    report={"status":"SELF_TEST_PASSED","blender_version":bpy.app.version_string,
        "action":act.name,"frame_range":frame_range(act),
        "note":"Blender action assignment smoke test passed; Mixamo FBX inputs are not required for this check."}
    with open(os.path.join(OUT_DIR,"mixamo-library-report.json"),"w",encoding="utf-8") as f: json.dump(report,f,indent=2)
    print("MIXAMO_LIBRARY_SELF_TEST_PASSED")

def build_library():
    character=os.path.join(ASSET_DIR,"character.fbx")
    clips=sorted(glob.glob(os.path.join(ACTION_DIR,"*.fbx")))
    if not os.path.isfile(character): raise RuntimeError("Missing assets/mixamo/character.fbx; see assets/mixamo/README.md")
    if not clips: raise RuntimeError("No FBX actions in assets/mixamo/actions/")
    clear_scene()
    base_objects=import_fbx(character,use_anim=False)
    base_rigs=armatures(base_objects)
    if len(base_rigs)!=1: raise RuntimeError("Expected exactly one character armature; found %d"%len(base_rigs))
    base=base_rigs[0]; base_bones={b.name for b in base.data.bones}; catalog=[]
    for path in clips:
        before_actions=set(bpy.data.actions)
        imported=import_fbx(path,use_anim=True)
        rigs=armatures(imported); new_actions=list(set(bpy.data.actions)-before_actions)
        clip_name=os.path.splitext(os.path.basename(path))[0]
        source=rigs[0] if rigs else None
        action=source.animation_data.action if source and source.animation_data else (new_actions[0] if new_actions else None)
        if action is None:
            remove_objects(imported); raise RuntimeError("No animation action found in "+clip_name)
        source_bones={b.name for b in source.data.bones} if source else set()
        common=base_bones.intersection(source_bones) if source_bones else set()
        coverage=len(common)/max(1,len(base_bones))
        if coverage<.65:
            remove_objects(imported)
            raise RuntimeError("Rig mismatch for %s: %.0f%% matching bone names; download all clips with the same Mixamo rig"%(clip_name,coverage*100))
        action.name="MIXAMO_"+clip_name; action.use_fake_user=True
        base.animation_data_create()
        try: base.animation_data.action=action
        except Exception as exc:
            remove_objects(imported); raise RuntimeError("Could not bind %s: %s"%(clip_name,exc))
        if base.animation_data.action!=action:
            remove_objects(imported); raise RuntimeError("Action binding verification failed for "+clip_name)
        fr=frame_range(action)
        catalog.append({"name":clip_name,"action":action.name,"source_file":os.path.basename(path),
            "frame_start":fr[0],"frame_end":fr[1],"frame_count":max(1,fr[1]-fr[0]+1),
            "base_bone_count":len(base_bones),"matching_bone_count":len(common),"bone_coverage":round(coverage,4)})
        remove_objects(imported); base.animation_data.action=None
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR,"wise-lab-mixamo-action-library.blend"))
    report={"status":"IMPORT_AND_BIND_PASSED","blender_version":bpy.app.version_string,
        "character":os.path.basename(character),"rig":base.name,"bone_count":len(base_bones),
        "action_count":len(catalog),"actions":catalog,
        "next_step":"Review the imported actions visually before connecting them to the hybrid compositor."}
    with open(os.path.join(OUT_DIR,"mixamo-library-report.json"),"w",encoding="utf-8") as f: json.dump(report,f,indent=2)
    print("MIXAMO_ACTION_LIBRARY_IMPORTED",len(catalog))

if __name__=="__main__":
    if "--self-test" in cli_args(): self_test()
    else: build_library()
