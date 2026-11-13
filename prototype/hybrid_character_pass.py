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


# 3D desk props rendered in the same pass as the character so hands and objects share depth.
def cube(name, location, dimensions, material, bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o=bpy.context.object; o.name=name; o.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new("soft manufactured edges","BEVEL"); mod.width=bevel; mod.segments=3
        o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
    return o

laptopBody=mat("laptop graphite",(.075,.095,.12))
laptopKeys=mat("keyboard keys",(.20,.23,.27))
screenMat=mat("screen deep blue",(.018,.045,.075))
screenGlow=mat("screen content glow",(.10,.32,.43))
ceramic=mat("warm ceramic",(.72,.68,.59))
coffee=mat("coffee",(.12,.055,.028))
paper=mat("notebook ivory",(.82,.77,.65))
penMat=mat("pen dark teal",(.035,.18,.20))
# Desk surface in the illustrated plate maps to z ~= 2.15 in this camera.
laptopBase=cube("3D laptop base",(1.02,-.40,2.18),(.92,.58,.055),laptopBody,.035)
laptopScreen=cube("3D laptop screen",(1.02,-.14,2.43),(.92,.055,.48),laptopBody,.035)
laptopDisplay=cube("laptop illuminated display",(1.02,-.172,2.43),(.82,.012,.38),screenMat,.012)
# A restrained interface glow makes the screen readable without text clutter.
screenBar=cube("screen interface accent",(1.02,-.181,2.55),(.48,.006,.018),screenGlow,.004)
for row in range(3):
    for col in range(11):
        cube("individual keyboard key",(0.66+col*.071,-.47-row*.105,2.213),(.047,.055,.009),laptopKeys,.006)
# Notebook, pen and coffee mug make the desk feel occupied and give later scenes usable props.
notebook=cube("closed notebook",(2.10,-.34,2.185),(.46,.34,.045),paper,.018)
notebookCover=cube("notebook cover",(2.10,-.34,2.209),(.47,.35,.018),laptopBody,.012)
pen=cube("pen on notebook",(2.12,-.37,2.229),(.36,.018,.012),penMat,.006)
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.105,depth=.22,location=(2.72,-.35,2.30))
mug=bpy.context.object; mug.name="ceramic coffee mug"; mug.data.materials.append(ceramic)
bev=mug.modifiers.new("mug softened rim","BEVEL"); bev.width=.012; bev.segments=3
bpy.ops.mesh.primitive_torus_add(major_radius=.075,minor_radius=.018,major_segments=24,minor_segments=10,location=(2.84,-.35,2.31))
handle=bpy.context.object; handle.name="coffee mug handle"; handle.data.materials.append(ceramic)
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.083,depth=.008,location=(2.72,-.35,2.414))
coffeeTop=bpy.context.object; coffeeTop.name="coffee surface"; coffeeTop.data.materials.append(coffee)

# Smartphone prop: upright on the desk, with a readable screen and a subtle incoming notification.
phoneBodyMat=mat("phone graphite casing",(.025,.035,.05))
phoneScreenMat=mat("phone glass screen",(.012,.025,.04))
phoneUI=mat("phone notification panel",(.12,.28,.34))
phoneGlow=mat("phone notification glow",(.12,.65,.78))
phoneBody=cube("smartphone casing",(.30,-.47,2.405),(.235,.075,.43),phoneBodyMat,.035)
phoneGlass=cube("smartphone glass",(.30,-.512,2.405),(.205,.012,.395),phoneScreenMat,.022)
phoneSpeaker=cube("phone speaker",(.30,-.520,2.585),(.055,.006,.009),laptopKeys,.003)
phoneBanner=cube("phone notification banner",(.30,-.522,2.455),(.166,.006,.075),phoneUI,.012)
phoneBannerLine=cube("notification text line",(.31,-.526,2.462),(.105,.004,.008),phoneGlow,.002)
phoneBadge=ball("notification badge",(.025,.012,.025),mat("notification coral",(.92,.20,.16)))
phoneBadge.location=(.375,-.528,2.50)
phoneHome=cube("phone home indicator",(.30,-.521,2.225),(.055,.004,.004),laptopKeys,.002)
# A small pool of cool light anchors the phone to the desk and gives its alert a visible cue.
bpy.ops.object.light_add(type="AREA",location=(.30,-.62,2.62))
phoneLight=bpy.context.object; phoneLight.name="phone notification light"; phoneLight.data.energy=18
phoneLight.data.color=(.22,.58,.82); phoneLight.data.shape="DISK"; phoneLight.data.size=.45
phoneLight.rotation_euler=(radians(18),0,0)

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
# Readable front-facing face: layered whites, irises, pupils, brows, nose, mouth and ears.
eyeWhite=mat("warm eye whites",(.92,.86,.75)); irisMat=mat("deep brown irises",(.12,.055,.028))
pupilMat=mat("dark pupils",(.012,.009,.008)); browMat=hair; mouthMat=mat("mouth",(.20,.065,.055))
ears=[ball("left ear",(.065,.055,.09),skin),ball("right ear",(.065,.055,.09),skin)]
eyes=[ball("left eye white",(.064,.025,.047),eyeWhite),ball("right eye white",(.064,.025,.047),eyeWhite)]
irises=[ball("left iris",(.027,.014,.030),irisMat),ball("right iris",(.027,.014,.030),irisMat)]
pupils=[ball("left pupil",(.014,.009,.020),pupilMat),ball("right pupil",(.014,.009,.020),pupilMat)]
brows=[ball("left eyebrow",(.072,.022,.018),browMat),ball("right eyebrow",(.072,.022,.018),browMat)]
nose=ball("nose",(.038,.040,.060),skin)
mouth=ball("mouth",(.060,.016,.014),mouthMat)
# Tiny cheek forms help the face read in profile and under soft lighting.
cheeks=[ball("left cheek",(.055,.018,.035),skin),ball("right cheek",(.055,.018,.035),skin)]
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
 # Face points toward camera (-Y); all features are re-positioned from the animated head anchor.
 for i,side in enumerate((-1,1)):
  x=rootx+side*.105
  eyes[i].location=(x,-.274,headz+.025)
  irises[i].location=(x+.008,-.300,headz+.020)
  pupils[i].location=(x+.010,-.313,headz+.020)
  brows[i].location=(rootx+side*.108,-.285,headz+.115)
  ears[i].location=(rootx+side*.292,-.005,headz-.015)
  cheeks[i].location=(rootx+side*.155,-.263,headz-.095)
 nose.location=(rootx,-.302,headz-.055)
 mouth.location=(rootx,-.292,headz-.158)
 # Natural periodic blink; keep the iris/pupil compressed with the eyelid.
 blinkPhase=frame%96
 blink=0.12 if blinkPhase in (0,1,2) else (0.45 if blinkPhase in (95,3) else 1.0)
 for eye in eyes: eye.scale.z=.047*blink
 for iris in irises: iris.scale.z=.030*blink
 for pupil in pupils: pupil.scale.z=.020*blink
 # Arm movement: natural swing while walking; right hand reaches the desktop in the final beat.
 shoulderL=(rootx-.36,0,shoulderz+.02); shoulderR=(rootx+.36,0,shoulderz+.02)
 walkSwing=math.sin(frame*.36)*.18*(1-sit)
 elbowL=mix((rootx-.56,0,shoulderz-.34),(rootx-.42,0,shoulderz-.30),sit)
 wristL=mix((rootx-.50,-.02,shoulderz-.70),(rootx-.18,-.10,1.10),sit)
 elbowR=mix((rootx+.56,0,shoulderz-.34),(rootx+.42,-.22,1.78),sit)
 wristR=mix((rootx+.50,-.02,shoulderz-.70),(rootx+.98,-.48,2.225),sit)
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

 # Brief notification pulse and restrained vibration; the phone remains planted on the desk.
 alert=smooth(0,1,(frame-112)/7)*(1-smooth(0,1,(frame-139)/8))
 pulse=.72+.28*(.5+.5*math.sin(frame*.48))
 def set_emission(material, color, strength):
  bs=material.node_tree.nodes.get("Principled BSDF")
  color_socket=bs.inputs.get("Emission Color") or bs.inputs.get("Emission")
  strength_socket=bs.inputs.get("Emission Strength")
  if color_socket: color_socket.default_value=(*color,1)
  if strength_socket: strength_socket.default_value=strength
 set_emission(phoneUI,(.08,.42,.55),.18*alert*pulse)
 set_emission(phoneGlow,(.10,.75,.95),.45*alert*pulse)
 phoneBadge.scale=(.025,.012,.025) if alert>.05 else (.001,.001,.001)
 phoneBody.rotation_euler[1]=.018*math.sin(frame*2.4)*alert
 phoneGlass.rotation_euler[1]=phoneBody.rotation_euler[1]
 phoneBanner.rotation_euler[1]=phoneBody.rotation_euler[1]
 phoneBannerLine.rotation_euler[1]=phoneBody.rotation_euler[1]
 phoneBadge.location=(.375,-.528,2.50)
 phoneLight.data.energy=18*alert*pulse

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
