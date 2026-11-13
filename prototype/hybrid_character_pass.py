import bpy, math, os
from mathutils import Vector
from math import radians

# WISE-LAB hybrid character pass: connected overlapping forms with endpoint-driven limbs.
# The illustrated room remains a separate 2D background/compositing layer.
OUT="renders/character"; os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine="BLENDER_EEVEE"
s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100
s.render.fps=24; s.frame_start=1; s.frame_end=168; s.eevee.taa_render_samples=8
s.render.image_settings.file_format="PNG"; s.render.image_settings.color_mode="RGBA"; s.render.film_transparent=True
s.view_settings.view_transform="Standard"; s.view_settings.look="Medium High Contrast"

def mat(name,color):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1); bs.inputs["Roughness"].default_value=.82
 return m
skin=mat("warm brown skin",(.55,.31,.22)); hoodie=mat("charcoal hoodie",(.055,.07,.095))
pants=mat("black denim",(.018,.025,.04)); hair=mat("black hair",(.012,.015,.02)); shoe=mat("dark sneakers",(.06,.07,.085))
def ball(name,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16)
 o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); bpy.ops.object.shade_smooth()
 return o
def segment(name,radius,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=1)
 o=bpy.context.object; o.name=name; o.data.materials.append(material)
 b=o.modifiers.new("rounded joint transitions","BEVEL"); b.width=radius*.88; b.segments=5
 o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
 return o
def place_ball(o,center):
 o.location=center
def place_segment(o,a,b):
 a=Vector(a); b=Vector(b); d=b-a
 o.location=(a+b)*.5; o.rotation_mode="QUATERNION"; o.rotation_quaternion=d.to_track_quat("Z","Y"); o.dimensions=(o.dimensions.x,o.dimensions.y,d.length)

# Camera frames a large, readable character while preserving the desk in the right side of the room.
bpy.ops.object.camera_add(location=(0,-12,2.45))
cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.ortho_scale=7.2
cam.rotation_euler=(radians(90),0,0); s.camera=cam

# Main silhouette: overlapping torso/neck/head and rounded shoulder/hip joints.
torso=ball("continuous hoodie torso",(.43,.27,.62),hoodie)
pelvis=ball("hip connection",(.36,.25,.25),pants)
neck=ball("neck",(.13,.14,.16),skin)
head=ball("head",(.30,.27,.36),skin)
haircap=ball("messy hair",(.32,.29,.20),hair)
fringe=ball("front hair",(.23,.10,.12),hair)
# Face detail facing camera (-Y).
eye1=ball("left eye",(.026,.018,.032),skin); eye2=ball("right eye",(.026,.018,.032),skin)
# Rounded limbs built from overlapping upper/lower sections; endpoints are updated as a single kinematic pose.
limbs={}
for name,r,m in [
 ("upperL",.135,hoodie),("foreL",.105,hoodie),("upperR",.135,hoodie),("foreR",.105,hoodie),
 ("thighL",.16,pants),("shinL",.12,pants),("thighR",.16,pants),("shinR",.12,pants)]:
 limbs[name]=segment(name,r,m)
joints={}
for name,r,m in [("shoulderL",.14,hoodie),("elbowL",.11,hoodie),("wristL",.085,skin),
 ("shoulderR",.14,hoodie),("elbowR",.11,hoodie),("wristR",.085,skin),
 ("hipL",.16,pants),("kneeL",.13,pants),("ankleL",.11,pants),
 ("hipR",.16,pants),("kneeR",.13,pants),("ankleR",.11,pants)]:
 joints[name]=ball(name,(r,r,r),m)
hands=[ball("left hand",(.11,.085,.075),skin),ball("right hand",(.11,.085,.075),skin)]
feet=[ball("left sneaker",(.22,.30,.11),shoe),ball("right sneaker",(.22,.30,.11),shoe)]

def smooth(a,b,t):
 t=max(0,min(1,t)); return a+(b-a)*(t*t*(3-2*t))
def mix(a,b,t): return tuple(smooth(x,y,t) for x,y in zip(a,b))
def pose(frame):
 # Walk in toward the chair, brake, lower into a seated pose, then reach to the laptop.
 walk=smooth(0,1,(frame-1)/48)
 sit=smooth(0,1,(frame-68)/35)
 rootx=-1.75+1.25*walk
 basez=smooth(0,1,(frame-68)/35)
 bob=(math.sin(frame*.42)*.045)*(1-sit) if frame<70 else 0
 hipz=smooth(1.02,.88,basez)+bob
 shoulderz=smooth(1.92,1.48,basez)+bob
 headz=smooth(2.43,2.02,basez)+bob
 # Feet plant during approach; seated legs bend forward with knees and shins.
 stride=math.sin(frame*.36)*.22*(1-smooth(0,1,(frame-35)/25))
 hipL=(rootx-.18,0,hipz); hipR=(rootx+.18,0,hipz)
 kneeL=mix((rootx-.20,0,.55),(rootx+.12,-.02,.57),sit); kneeR=mix((rootx+.20,0,.55),(rootx+.48,-.02,.57),sit)
 ankleL=mix((rootx-.20,-.02,.12),(rootx+.30,-.03,.12),sit); ankleR=mix((rootx+.20,-.02,.12),(rootx+.68,-.03,.12),sit)
 if frame<70:
  kneeL=(rootx-.20+stride,0,.55); kneeR=(rootx+.20-stride,0,.55)
  ankleL=(rootx-.20+stride*1.3,-.02,.12); ankleR=(rootx+.20-stride*1.3,-.02,.12)
 # torso/head positions; shoulder anchors follow torso.
 torso.location=(rootx,0,shoulderz-.36); pelvis.location=(rootx,0,hipz)
 neck.location=(rootx,0,headz-.39); head.location=(rootx,-.015,headz)
 haircap.location=(rootx,.005,headz+.22); fringe.location=(rootx,-.23,headz+.14)
 eye1.location=(rootx-.105,-.278,headz+.015); eye2.location=(rootx+.105,-.278,headz+.015)
 # Arm movement: natural swing while walking; right hand reaches the desktop in the final beat.
 shoulderL=(rootx-.36,0,shoulderz+.02); shoulderR=(rootx+.36,0,shoulderz+.02)
 walkSwing=math.sin(frame*.36)*.18*(1-sit)
 elbowL=mix((rootx-.56,0,shoulderz-.34),(rootx-.42,0,shoulderz-.30),sit)
 wristL=mix((rootx-.50,-.02,shoulderz-.70),(rootx-.18,-.10,1.10),sit)
 elbowR=mix((rootx+.56,0,shoulderz-.34),(rootx+.53,-.02,shoulderz-.25),sit)
 wristR=mix((rootx+.50,-.02,shoulderz-.70),(rootx+.88,-.18,1.16),sit)
 if frame<65:
  elbowL=(rootx-.56,0,shoulderz-.34+walkSwing); wristL=(rootx-.50,-.02,shoulderz-.70+walkSwing)
  elbowR=(rootx+.56,0,shoulderz-.34-walkSwing); wristR=(rootx+.50,-.02,shoulderz-.70-walkSwing)
 for n,p in [("shoulderL",shoulderL),("elbowL",elbowL),("wristL",wristL),("shoulderR",shoulderR),("elbowR",elbowR),("wristR",wristR),
             ("hipL",hipL),("kneeL",kneeL),("ankleL",ankleL),("hipR",hipR),("kneeR",kneeR),("ankleR",ankleR)]:
  joints[n].location=p
 for n,a,b in [("upperL",shoulderL,elbowL),("foreL",elbowL,wristL),("upperR",shoulderR,elbowR),("foreR",elbowR,wristR),
               ("thighL",hipL,kneeL),("shinL",kneeL,ankleL),("thighR",hipR,kneeR),("shinR",kneeR,ankleR)]:
  place_segment(limbs[n],a,b)
 hands[0].location=(wristL[0],wristL[1]-.04,wristL[2]); hands[1].location=(wristR[0],wristR[1]-.04,wristR[2])
 feet[0].location=(ankleL[0]+.08,-.12,ankleL[2]); feet[1].location=(ankleR[0]+.08,-.12,ankleR[2])
 feet[0].rotation_euler[1]=-.08; feet[1].rotation_euler[1]=-.08

# Frame handler guarantees continuous connected endpoint motion without detached object-origin rotations.
def update(scene): pose(scene.frame_current)
s.frame_set(1); update(s)
if update not in bpy.app.handlers.frame_change_pre: bpy.app.handlers.frame_change_pre.append(update)
# Soft key/fill lighting.
for loc,power,size in [((-3,-4,6),650,5),((3,1,4),350,4)]:
 bpy.ops.object.light_add(type="AREA",location=loc); light=bpy.context.object
 light.data.energy=power; light.data.shape="DISK"; light.data.size=size; light.rotation_euler=(radians(25),0,radians(20))
s.render.filepath=os.path.abspath(OUT+"/frame_")
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("renders/hybrid-character.blend"))
bpy.ops.render.render(animation=True)
print("HYBRID_CHARACTER_PASS_COMPLETE")
