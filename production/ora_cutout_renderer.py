"""Painted ORA layers to a Blender armature and MP4. No primitive fallback."""
import argparse, json, math, sys, zipfile, xml.etree.ElementTree as ET, subprocess
from pathlib import Path
import bpy

def cli():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    for flag,kw in [("--ora",{"required":True}),("--rig",{"required":True}),("--out",{"default":"renders/preview.mp4"}),("--duration",{"type":float,"default":10}),("--fps",{"type":int,"default":24}),("--width",{"type":int,"default":1280}),("--height",{"type":int,"default":720})]: p.add_argument(flag,**kw)
    return p.parse_args(av)

def unpack_ora(path,tmp):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read("stack.xml")); w,h=int(root.get("w",0)),int(root.get("h",0)); layers=[]; serial=[0]
        def walk(node):
            for child in list(node):
                if child.tag=="layer":
                    src=child.get("src")
                    if src:
                        serial[0]+=1; dst=tmp/("%03d_%s.png"%(serial[0],child.get("name","layer").replace("/","_")))
                        dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(z.read(src))
                        layers.append({"name":child.get("name","layer"),"src":str(dst),"x":int(child.get("x",0)),"y":int(child.get("y",0)),"opacity":float(child.get("opacity",1)),"visible":child.get("visibility","visible")!="hidden"})
                    walk(child)
                else: walk(child)
        walk(root)
    if not w or not h or not layers: raise RuntimeError("ORA has no canvas or paint layers")
    return w,h,layers

def reset():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)

def make_rig(rig,w,h):
    data=bpy.data.armatures.new("PaintedRig"); arm=bpy.data.objects.new("PaintedRig",data); bpy.context.collection.objects.link(arm)
    bpy.context.view_layer.objects.active=arm; arm.select_set(True); bpy.ops.object.mode_set(mode="EDIT")
    for name,s in rig["bones"].items():
        b=data.edit_bones.new(name); hx,hy=s["head"]; tx,ty=s["tail"]
        b.head=(hx-w/2,0,h/2-hy); b.tail=(tx-w/2,0,h/2-ty)
        if s.get("parent"):
            if s["parent"] not in data.edit_bones: raise RuntimeError("Missing parent bone "+s["parent"])
            b.parent=data.edit_bones[s["parent"]]; b.use_connect=False
    bpy.ops.object.mode_set(mode="OBJECT"); return arm

def material(name,path,opacity):
    img=bpy.data.images.load(path,check_existing=True); m=bpy.data.materials.new(name+"_paint"); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; n.clear()
    out=n.new("ShaderNodeOutputMaterial"); tex=n.new("ShaderNodeTexImage"); tex.image=img
    emit=n.new("ShaderNodeEmission"); trans=n.new("ShaderNodeBsdfTransparent"); mul=n.new("ShaderNodeMath"); mul.operation="MULTIPLY"; mul.inputs[1].default_value=opacity
    mix=n.new("ShaderNodeMixShader")
    l.new(tex.outputs["Color"],emit.inputs["Color"]); l.new(tex.outputs["Alpha"],mul.inputs[0]); l.new(mul.outputs[0],mix.inputs[0])
    l.new(trans.outputs[0],mix.inputs[1]); l.new(emit.outputs[0],mix.inputs[2]); l.new(mix.outputs[0],out.inputs["Surface"])
    if hasattr(m,"surface_render_method"): m.surface_render_method="DITHERED"
    elif hasattr(m,"blend_method"): m.blend_method="BLEND"
    return m

def add_layer(layer,mapping,arm,bones,w,h,depth):
    if not layer["visible"]: return
    name=layer["name"]; spec=mapping.get(name); bone=spec["bone"] if spec else None
    if bone:
        if bone not in bones: raise RuntimeError("Missing bone %s for layer %s"%(bone,name))
        px,py=spec["pivot"]; bx,by=bones[bone]["head"]
        if abs(px-bx)>3 or abs(py-by)>3: raise RuntimeError("Pivot for %s must match bone %s head"%(name,bone))
    img=bpy.data.images.load(layer["src"],check_existing=True); iw,ih=img.size; x,y=layer["x"],layer["y"]
    lft,rgt,top,bot=x-w/2,x+iw-w/2,h/2-y,h/2-y-ih
    mesh=bpy.data.meshes.new(name+"_mesh"); mesh.from_pydata([(lft,0,top),(rgt,0,top),(rgt,0,bot),(lft,0,bot)],[],[(0,1,2,3)]); mesh.update()
    uv=mesh.uv_layers.new(name="PaintUV")
    for poly in mesh.polygons:
        for i,co in zip(poly.loop_indices,[(0,1),(1,1),(1,0),(0,0)]): uv.data[i].uv=co
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj); obj.location.y=depth
    obj.data.materials.append(material(name,layer["src"],layer["opacity"]))
    if bone:
        vg=obj.vertex_groups.new(name=bone); vg.add([0,1,2,3],1.0,"REPLACE")
        mod=obj.modifiers.new("Painted layer armature","ARMATURE"); mod.object=arm

def animate(arm,fps,duration):
    end=max(2,round(fps*duration)); scene=bpy.context.scene; scene.frame_start=1; scene.frame_end=end
    keys=[(1,0,0),(round(end*.28),-.22,.30),(round(end*.58),-.52,.68),(round(end*.82),-.12,.14),(end,0,0)]
    for frame,shoulder,elbow in keys:
        scene.frame_set(frame)
        for name,angle in [("upper_arm_R",shoulder),("forearm_R",elbow)]:
            b=arm.pose.bones.get(name)
            if b: b.rotation_mode="XYZ"; b.rotation_euler=(0,0,angle); b.keyframe_insert(data_path="rotation_euler",frame=frame,group=name)
    if arm.animation_data and arm.animation_data.action:
        for fc in arm.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation="BEZIER"

def main():
    a=cli(); ora=Path(a.ora).resolve(); rigfile=Path(a.rig).resolve()
    if not ora.is_file() or not rigfile.is_file(): raise FileNotFoundError("A layered .ora artwork file and rig JSON are required; no shape fallback.")
    rig=json.loads(rigfile.read_text(encoding="utf-8")); needed={"root","torso","head","upper_arm_R","forearm_R"}
    if not needed.issubset(rig.get("bones",{})): raise RuntimeError("Rig missing required motion bones: "+str(sorted(needed-set(rig.get("bones",{})))))
    reset(); w,h,layers=unpack_ora(ora,Path("/tmp/wiselab_ora")); canvas=rig.get("canvas",{})
    if canvas.get("width")!=w or canvas.get("height")!=h: raise RuntimeError("Rig canvas size does not match ORA canvas")
    mapping=rig.get("layers",{}); names={x["name"] for x in layers}
    missing=sorted({n for n,s in mapping.items() if s.get("required")}-names)
    if missing: raise RuntimeError("ORA missing required painted layers: "+", ".join(missing))
    arm=make_rig(rig,w,h)
    for i,item in enumerate(layers): add_layer(item,mapping,arm,rig["bones"],w,h,i*.002)
    animate(arm,a.fps,a.duration); scene=bpy.context.scene
    engines=[e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    scene.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
    scene.render.resolution_x=a.width; scene.render.resolution_y=a.height; scene.render.resolution_percentage=100; scene.render.fps=a.fps
    scene.render.image_settings.file_format="PNG"; scene.render.image_settings.color_mode="RGBA"; scene.render.film_transparent=False
    scene.world.use_nodes=True; scene.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.035,.045,.065,1)
    bpy.ops.object.camera_add(location=(0,-max(w,h)*1.8,0)); cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.ortho_scale=min(w,h*a.width/a.height)*1.08
    cam.rotation_euler=(math.radians(90),0,0); scene.camera=cam
    out=Path(a.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True); frames=out.parent/"frames"; frames.mkdir(parents=True,exist_ok=True)
    scene.render.filepath=str(frames/"frame_"); bpy.ops.render.render(animation=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(a.fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
    print("RENDER_OK=%s LAYERS=%d FRAMES=%d"%(out,len(layers),scene.frame_end))

if __name__=="__main__": main()
