import bpy, math, os
from mathutils import Vector
from math import radians

OUT=os.environ.get("WISE_OUTPUT","renders/blender-benchmark.mp4")
os.makedirs(os.path.dirname(os.path.abspath(OUT)),exist_ok=True)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE"
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.fps=24; scene.frame_start=1; scene.frame_end=360
scene.render.image_settings.file_format="FFMPEG"; scene.render.ffmpeg.format="MPEG4"; scene.render.ffmpeg.codec="H264"; scene.render.ffmpeg.constant_rate_factor="HIGH"; scene.render.ffmpeg.ffmpeg_preset="GOOD"
scene.render.filepath=os.path.abspath(OUT); scene.world.color=(.055,.075,.11)
scene.view_settings.view_transform="Standard"; scene.view_settings.look="Medium High Contrast"
def mat(name,color,rough=.72,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1); bs.inputs["Roughness"].default_value=rough; bs.inputs["Metallic"].default_value=metal
 return m
navy=mat("Hoodie",(0.075,.12,.19)); blue=mat("Trousers",(.045,.075,.12)); skin=mat("Warm skin",(.52,.29,.20)); hair=mat("Hair",(.018,.025,.04)); shoe=mat("Sneakers",(.025,.035,.05)); sole=mat("Soles",(.72,.74,.71)); glass=mat("Phone glass",(.012,.025,.04),.18,.25); screen=mat("Phone screen",(.13,.48,.52),.25); wood=mat("Walnut",(.24,.12,.07)); wall=mat("Wall",(.22,.31,.38)); floor=mat("Floor",(.12,.16,.19)); windowmat=mat("Evening window",(.11,.22,.32),.3); lampmat=mat("Lamp glow",(1,.58,.24),.35)
def cube(name,loc,scale,material,bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(material)
 if bevel:
  m=o.modifiers.new("Soft edges","BEVEL"); m.width=bevel; m.segments=3; o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
 return o
def uv(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o
def cyl_between(name,a,b,r,material):
 mid=(Vector(a)+Vector(b))/2; v=Vector(b)-Vector(a)
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=v.length,location=mid); o=bpy.context.object; o.name=name; o.rotation_mode="QUATERNION"; o.rotation_quaternion=v.to_track_quat("Z","Y"); o.data.materials.append(material)
 m=o.modifiers.new("Rounded ends","BEVEL"); m.width=r*.55; m.segments=3; o.modifiers.new("Normals","WEIGHTED_NORMAL"); return o
# Layered room set with window, desk, chair and practical light.
cube("Floor",(0,0,-.12),(12,9,.24),floor,.03); cube("Back wall",(0,2,2.6),(12,.18,5.4),wall,.03)
cube("Window recess",(-3.2,1.88,2.9),(2.6,.06,2.3),navy,.02); cube("Window glass",(-3.2,1.82,2.9),(2.42,.04,2.12),windowmat,.01)
for x in (-4.42,-3.2,-1.98): cube("Window mullion",(x,1.77,2.9),(.055,.08,2.2),wood,.01)
cube("Window crossbar",(-3.2,1.76,2.9),(2.45,.08,.055),wood,.01)
cube("Desk top",(1.75,-.05,.92),(2.7,1.15,.16),wood,.07)
for x in (.65,2.85): cube("Desk leg",(x,-.02,.45),(.12,.85,.9),wood,.025)
paper=mat("Notebook paper",(.82,.79,.68)); cube("Notebook",(1.25,-.18,1.02),(.48,.34,.035),paper,.01)
cube("Phone body",(2.25,-.18,1.06),(.19,.34,.035),glass,.025); cube("Phone display",(2.25,-.18,1.081),(.16,.29,.008),screen,.01)
cube("Chair seat",(-.1,.12,.58),(.75,.7,.13),wood,.05); cube("Chair back",(-.1,.43,1),(.75,.12,.9),wood,.05)
cube("Lamp base",(2.85,.12,1.03),(.32,.28,.06),wood,.04); cyl_between("Lamp stem",(2.85,.12,1.05),(2.85,.12,1.55),.035,wood); uv("Lamp shade",(2.85,.12,1.57),(.25,.22,.16),lampmat)
# Reusable articulated armature.
ad=bpy.data.armatures.new("WISE-LAB humanoid rig"); rig=bpy.data.objects.new("WISE-LAB | reusable character rig",ad); bpy.context.collection.objects.link(rig); bpy.context.view_layer.objects.active=rig; rig.select_set(True); bpy.ops.object.mode_set(mode="EDIT")
bones={"root":((0,0,.08),(0,0,.95),None),"spine":((0,0,.85),(0,0,1.62),"root"),"neck":((0,0,1.55),(0,0,1.78),"spine"),"head":((0,0,1.72),(0,0,2.13),"neck"),"upper_arm.L":((-.27,0,1.52),(-.48,0,1.12),"spine"),"forearm.L":((-.48,0,1.12),(-.49,0,.78),"upper_arm.L"),"upper_arm.R":((.27,0,1.52),(.49,0,1.12),"spine"),"forearm.R":((.49,0,1.12),(.51,0,.78),"upper_arm.R"),"thigh.L":((-.15,0,.91),(-.17,0,.49),"root"),"shin.L":((-.17,0,.49),(-.17,0,.10),"thigh.L"),"thigh.R":((.15,0,.91),(.17,0,.49),"root"),"shin.R":((.17,0,.49),(.17,0,.10),"thigh.R")}
for name,(h,t,parent) in bones.items():
 b=ad.edit_bones.new(name); b.head=h; b.tail=t
 if parent: b.parent=ad.edit_bones[parent]
bpy.ops.object.mode_set(mode="OBJECT"); rig.show_in_front=True; rig.display_type="WIRE"; rig.location=(-1.55,0,0)
def attach(obj,bone):
 bpy.context.view_layer.update(); world=obj.matrix_world.copy(); obj.parent=rig; obj.parent_type="BONE"; obj.parent_bone=bone; bpy.context.view_layer.update(); obj.matrix_world=world; return obj
def segment(name,bone,length,r,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=length,location=(0,0,length/2)); o=bpy.context.object; o.name=name; o.data.materials.append(material)
 m=o.modifiers.new("Rounded silhouette","BEVEL"); m.width=r*.8; m.segments=4; o.modifiers.new("Normals","WEIGHTED_NORMAL"); return attach(o,bone)
segment("Hoodie torso","spine",.78,.31,navy); segment("Neck","neck",.23,.11,skin)
for side in ("L","R"):
 segment("Upper arm "+side,"upper_arm."+side,.46,.105,navy); segment("Forearm "+side,"forearm."+side,.38,.085,navy)
 segment("Thigh "+side,"thigh."+side,.47,.14,blue); segment("Shin "+side,"shin."+side,.43,.105,blue)
 hand=uv("Hand "+side,(0,0,0),(.095,.085,.10),skin); attach(hand,"forearm."+side); hand.location=(0,0,.39)
 foot=uv("Sneaker "+side,(0,0,0),(.19,.12,.09),shoe); attach(foot,"shin."+side); foot.location=(0,-.035,-.02)
 soleob=uv("Sole "+side,(0,0,0),(.195,.125,.035),sole); attach(soleob,"shin."+side); soleob.location=(0,-.035,-.075)
head=uv("Head",(0,0,0),(.25,.23,.29),skin); attach(head,"head")
cap=uv("Messy hair",(0,0,0),(.265,.24,.16),hair); attach(cap,"head"); cap.location=(0,-.015,.19)
for x in (-.09,.09):
 eye=uv("Eye",(0,0,0),(.025,.018,.025),hair); attach(eye,"head"); eye.location=(x,-.218,.015)
# Phone object is a separately reusable prop; keyed from tabletop to hand zone.
prop=bpy.data.objects.new("Phone | grabbable prop",None); bpy.context.collection.objects.link(prop); prop.empty_display_type="CUBE"; prop.location=(2.25,-.18,1.11); prop.keyframe_insert(data_path="location",frame=1); prop.keyframe_insert(data_path="location",frame=264); prop.location=(.05,-.48,1.28); prop.keyframe_insert(data_path="location",frame=330); prop.keyframe_insert(data_path="location",frame=360)
body=cube("Animated phone body",(0,0,0),(.19,.34,.035),glass,.025); body.parent=prop; body.location=(0,0,0)
display=cube("Animated phone display",(0,0,0),(.16,.29,.008),screen,.01); display.parent=prop; display.location=(0,0,.022)
def pose(frame,loc,rots):
 scene.frame_set(frame); rig.location=loc; rig.keyframe_insert(data_path="location",frame=frame)
 for name,rot in rots.items():
  pb=rig.pose.bones[name]; pb.rotation_mode="XYZ"; pb.rotation_euler=rot; pb.keyframe_insert(data_path="rotation_euler",frame=frame)
# Walk toward desk, settle, reach and lift.
pose(1,(-1.75,0,0),{"thigh.L":(radians(22),0,0),"thigh.R":(radians(-22),0,0),"upper_arm.L":(radians(-18),0,0),"upper_arm.R":(radians(18),0,0)})
pose(24,(-1.25,0,0),{"thigh.L":(radians(-22),0,0),"thigh.R":(radians(22),0,0),"upper_arm.L":(radians(18),0,0),"upper_arm.R":(radians(-18),0,0)})
pose(48,(-.75,0,0),{"thigh.L":(0,0,0),"thigh.R":(0,0,0),"upper_arm.L":(0,0,0),"upper_arm.R":(0,0,0)})
pose(72,(-.72,0,0),{"spine":(radians(-3),0,0),"upper_arm.R":(radians(-12),0,0)})
pose(120,(-.72,0,0),{"spine":(radians(-3),0,0),"upper_arm.R":(radians(-12),0,0)})
pose(168,(-.72,0,0),{"upper_arm.R":(radians(-68),0,0),"forearm.R":(radians(-25),0,0),"spine":(radians(-5),0,0)})
pose(216,(-.72,0,0),{"upper_arm.R":(radians(-82),0,0),"forearm.R":(radians(-38),0,0),"spine":(radians(-6),0,0)})
pose(264,(-.72,0,0),{"upper_arm.R":(radians(-82),0,0),"forearm.R":(radians(-38),0,0)})
pose(330,(-.72,0,0),{"upper_arm.R":(radians(-42),0,0),"forearm.R":(radians(-15),0,0)})
pose(360,(-.72,0,0),{"upper_arm.R":(radians(-42),0,0),"forearm.R":(radians(-15),0,0)})
for ob in (rig,prop):
 if ob.animation_data and ob.animation_data.action:
  for fc in ob.animation_data.action.fcurves:
   for kp in fc.keyframe_points: kp.interpolation="BEZIER"
# Camera push-in and three-point lighting.
bpy.ops.object.camera_add(location=(0,-10.8,3)); cam=bpy.context.object; cam.data.lens=48; scene.camera=cam
def aim(obj,p): obj.rotation_euler=(Vector(p)-obj.location).to_track_quat("-Z","Y").to_euler()
aim(cam,(.05,0,1.25)); cam.keyframe_insert(data_path="location",frame=1); cam.keyframe_insert(data_path="rotation_euler",frame=1)
cam.location=(.2,-9.8,2.8); aim(cam,(.25,0,1.25)); cam.keyframe_insert(data_path="location",frame=360); cam.keyframe_insert(data_path="rotation_euler",frame=360)
for fc in cam.animation_data.action.fcurves:
 for kp in fc.keyframe_points: kp.interpolation="BEZIER"
bpy.ops.object.light_add(type="AREA",location=(-3,-4,6)); key=bpy.context.object; key.data.energy=850; key.data.shape="DISK"; key.data.size=5; aim(key,(0,0,1))
bpy.ops.object.light_add(type="AREA",location=(3,1,4)); fill=bpy.context.object; fill.data.energy=500; fill.data.color=(.48,.68,1); fill.data.size=4; aim(fill,(0,0,1))
bpy.ops.object.light_add(type="AREA",location=(2,-2,3)); practical=bpy.context.object; practical.data.energy=220; practical.data.color=(1,.55,.25); practical.data.size=2; aim(practical,(1,0,1))
scene.render.image_settings.color_mode="RGB"; scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT).replace(".mp4",".blend"))
bpy.ops.render.render(animation=True)
print("BENCHMARK_RENDERED",os.path.abspath(OUT))
