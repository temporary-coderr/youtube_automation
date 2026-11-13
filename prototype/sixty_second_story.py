import bpy, math, os
from mathutils import Vector
from math import radians

# WISE-LAB 60s story pilot: "The Hidden Cost of Always Being Available"
# Original stylized 3D character and six purpose-built environments.
OUT = "renders/pilot_frames"
os.makedirs(OUT, exist_ok=True)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine = "BLENDER_EEVEE_NEXT" if hasattr(s, "eevee") is False else "BLENDER_EEVEE"
s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100
s.render.fps=24; s.frame_start=1; s.frame_end=1440
s.render.image_settings.file_format="PNG"; s.render.image_settings.color_mode="RGBA"
s.render.film_transparent=False
s.render.image_settings.color_depth="8"
s.render.engine = "BLENDER_EEVEE"
if hasattr(s, "eevee"): s.eevee.taa_render_samples=16
s.view_settings.view_transform="Standard"
s.view_settings.look="Medium High Contrast"
s.world.color=(0.055,0.065,0.085)

def mat(name, color, rough=.8, emission=None):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1); bs.inputs["Roughness"].default_value=rough
    if emission:
        e=bs.inputs.get("Emission Color") or bs.inputs.get("Emission")
        if e: e.default_value=(*color,1)
        st=bs.inputs.get("Emission Strength")
        if st: st.default_value=emission
    return m

navy=mat("midnight navy",(.035,.065,.12)); wall=mat("warm plaster",(.72,.66,.57))
floor=mat("warm wood",(.25,.16,.12)); teal=mat("teal",(.04,.36,.38))
mustard=mat("mustard jacket",(.88,.48,.12)); skin=mat("warm skin",(.68,.39,.27))
hair=mat("deep auburn hair",(.16,.055,.035)); pants=mat("deep teal trousers",(.025,.12,.16))
shoe=mat("dark shoes",(.035,.04,.055)); white=mat("warm white",(.92,.88,.78))
phoneMat=mat("phone glass",(.012,.025,.04),.2); glow=mat("notification glow",(.12,.62,.85),.3,1.8)
wood=mat("furniture wood",(.32,.19,.12)); leaf=mat("plant green",(.10,.30,.16))
pink=mat("coral accent",(.85,.22,.20)); sky=mat("dusk sky",(.12,.23,.34))
def cube(name, loc, scale, material, bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(material)
    if bevel:
        b=o.modifiers.new("soft edges","BEVEL"); b.width=bevel; b.segments=3
        o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
    return o
def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o
def cyl(name, loc, radius, depth, material, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material)
    if rot: o.rotation_euler=rot
    b=o.modifiers.new("rounded edges","BEVEL"); b.width=min(radius*.25,.035); b.segments=3
    return o
def text_obj(body, loc, size, material):
    cu=bpy.data.curves.new("title typography","FONT"); cu.body=body; cu.size=size; cu.extrude=.002
    ob=bpy.data.objects.new(body,cu); s.collection.objects.link(ob); ob.location=loc; ob.data.materials.append(material); return ob

# Six independent scene stages laid out along X. Each gets its own camera composition.
centers=[0,16,32,48,64,80]
scene_names=["BEDROOM • 11:47 PM","CAFÉ • THE GROUP CHAT","OFFICE • ALWAYS ON","CITY • THE WALK HOME","PARK • A SMALL PAUSE","HOME • YOUR TIME"]
for idx,cx in enumerate(centers):
    bg=[navy,mat("cafe sage",(.30,.40,.35)),mat("office bluegray",(.25,.34,.43)),mat("city dusk",(.12,.20,.29)),mat("park dusk",(.12,.25,.22)),mat("calm home",(.34,.39,.38))][idx]
    cube(f"stage {idx} wall",(cx,2,3),(13,.5,6),bg,.02)
    cube(f"stage {idx} floor",(cx,0,-.18),(13,14,.35),floor,.02)
    # warm pools of practical light and distinctive environmental silhouettes
    if idx in (0,5):
        cube("window frame",(cx-3,1.68,3.2),(3.2,.12,2.8),wood,.04)
        cube("window night glass",(cx-3,1.60,3.2),(2.9,.08,2.5),sky,.02)
        for z in [2.5,3.7]: cube("window mullion",(cx-3,1.52,z),(.07,.08,2.5),white,.01)
        cube("bed frame",(cx-2,-.5,.55),(3.8,2.2,.45),wood,.12)
        cube("bed mattress",(cx-2,-.5,.86),(3.7,2.15,.35),white,.12)
        cube("pillow",(cx-3,-.25,1.10),(1.1,.8,.22),mustard,.12)
        cube("nightstand",(cx+3,-.2,.65),(1.3,1.1,1.3),wood,.08)
        cyl("lamp stem",(cx+3,-.2,1.55),.06,.65,wood)
        sphere("lamp shade",(cx+3,-.2,1.95),(.38,.38,.28),mustard)
        bpy.ops.object.light_add(type="AREA", location=(cx+3,-1,2.2))
        L=bpy.context.object; L.data.energy=150; L.data.shape="DISK"; L.data.size=3
    elif idx==1:
        for x in [-2,2]:
            cyl("cafe table pedestal",(cx+x,-.1,.55),.10,1.1,wood)
            cyl("cafe round table",(cx+x,-.1,1.12),.95,.12,wood)
            for dx in [-.65,.65]:
                cube("cafe chair",(cx+x+dx,.7,.65),(.65,.65,1.3),teal,.08)
        for x in [-4,0,4]:
            cube("cafe window",(cx+x,1.68,3.2),(2.4,.1,2.6),white,.04)
            cube("cafe glass",(cx+x,1.60,3.2),(2.15,.08,2.35),sky,.02)
        cyl("coffee cup",(cx-2,-.1,1.38),.16,.32,white)
    elif idx==2:
        cube("office desk",(cx,-.4,1.15),(5.8,1.3,.22),wood,.06)
        for x in [-2.5,2.5]: cube("desk leg",(cx+x,-.4,.55),(.16,.16,1.2),wood,.02)
        cube("monitor",(cx,-.1,2.15),(2.2,.16,1.45),navy,.06)
        cube("monitor screen",(cx,-.2,2.15),(2.02,.035,1.25),glow,.02)
        cube("office chair",(cx+2,-1,.85),(1.1,.8,1.5),teal,.15)
        for x in [-4,4]: cube("office window",(cx+x,1.68,3.4),(1.6,.1,3),sky,.03)
    elif idx==3:
        for x in [-4,-1,2,5]:
            cube("city building",(cx+x,2,2.2),(1.5,.8,4.4),navy,.02)
            for z in [1.2,2.2,3.2]: cube("lit building window",(cx+x,1.55,z),(.32,.05,.42),mustard,.01)
        cube("sidewalk",(cx,-.2,.02),(12,5,.15),mat("sidewalk concrete",(.28,.30,.32)),.02)
        cyl("street lamp pole",(cx+4,-.2,2.3),.06,4.6,wood)
        sphere("street lamp glow",(cx+4,-.2,4.55),(.25,.25,.22),mustard)
    elif idx==4:
        for x in [-4,4]:
            cyl("tree trunk",(cx+x,1,1.8),.22,3.6,wood)
            sphere("tree canopy",(cx+x,1,3.8),(1.3,.75,1.3),leaf)
        cube("park bench seat",(cx+2,-.2,.75),(2.4,.65,.18),wood,.06)
        for x in [cx+1.1,cx+2.9]: cube("bench leg",(x,-.2,.4),(.14,.55,.7),wood,.03)
        sphere("park light",(cx-3,-.2,4.3),(.22,.22,.22),mustard)
    # Plant silhouette for depth in each stage.
    if idx in (1,2,4):
        cyl("plant pot",(cx-5,-.1,.45),.35,.8,wood)
        for j in range(5):
            sphere("plant leaves",(cx-5+math.sin(j*1.2)*.35,-.1,1+j*.12),(.18,.16,.55),leaf)

# New recurring pilot character: Mira, 24, short auburn bob, mustard jacket, teal trousers.
# All body parts are grouped under a root empty so she can travel between sets.
root=bpy.data.objects.new("MIRA • character root",None); s.collection.objects.link(root)
def attach(o):
    o.parent=root
    return o
# Character faces camera (-Y), with readable layered facial features.
attach(sphere("Mira torso",(0,0,1.38),(.48,.30,.62),mustard))
attach(sphere("Mira neck",(0,-.01,1.94),(.15,.14,.16),skin))
attach(sphere("Mira head",(0,-.04,2.25),(.34,.29,.40),skin))
attach(sphere("Mira bob hair",(0,.02,2.48),(.37,.31,.27),hair))
attach(sphere("Mira side hair left",(-.30,-.02,2.25),(.11,.22,.28),hair))
attach(sphere("Mira side hair right",(.30,-.02,2.25),(.11,.22,.28),hair))
eyeWhite=mat("eye ivory",(.95,.88,.78)); iris=mat("iris",(.12,.055,.03)); black=mat("pupil",(.01,.008,.008))
for x in [-.12,.12]:
    attach(sphere("eye white",(x,-.315,2.29),(.065,.025,.045),eyeWhite))
    attach(sphere("iris",(x,-.342,2.29),(.027,.015,.03),iris))
    attach(sphere("pupil",(x,-.354,2.29),(.013,.009,.018),black))
    attach(sphere("eyebrow",(x,-.32,2.38),(.075,.025,.018),hair))
attach(sphere("Mira nose",(0,-.35,2.22),(.035,.045,.06),skin))
attach(sphere("Mira mouth",(0,-.338,2.12),(.06,.018,.014),pink))
# Lower body and shoes.
attach(sphere("Mira hips",(0,0,.88),(.39,.28,.30),pants))
for x in [-.19,.19]:
    attach(cube("Mira trouser leg",(x,0,.48),(.28,.32,.78),pants,.10))
    attach(sphere("Mira shoe",(x,-.12,.12),(.20,.32,.12),shoe))
# Arms, shoulder joints and hands, built as capsule-like tapered cylinders.
def limb(name,a,b,r,material,parent=root):
    mid=(Vector(a)+Vector(b))*.5; d=Vector(b)-Vector(a)
    o=cyl(name,mid,r,d.length,material)
    o.rotation_euler=d.to_track_quat("Z","Y").to_euler(); o.parent=parent
    return o
arm_objs=[]
for side in [-1,1]:
    shoulder=(side*.43,0,1.72); elbow=(side*.58,-.02,1.25); hand=(side*.62,-.08,.98)
    upper=limb("Mira jacket upper arm",shoulder,elbow,.15,mustard)
    fore=limb("Mira jacket forearm",elbow,hand,.12,mustard)
    palm=attach(sphere("Mira hand",hand,(.12,.10,.09),skin))
    arm_objs.append((upper,fore,palm,side))
# Signature smartphone prop attached to her right hand initially; it can be set on surfaces.
phone=attach(cube("Mira smartphone",( .66,-.18,1.02),(.22,.09,.40),phoneMat,.035))
attach(cube("phone notification panel",(.66,-.232,1.06),(.17,.012,.11),glow,.01))
# A small bag gives silhouette and story continuity.
attach(cube("Mira shoulder bag",(-.52,.05,1.0),(.42,.22,.46),teal,.08))

# Camera and lights.
bpy.ops.object.camera_add(location=(0,-13,3.1)); cam=bpy.context.object
cam.data.type="ORTHO"; cam.data.ortho_scale=9.0
s.camera=cam
def aim(x,z=1.65):
    cam.location=(x,-13,z+1.3)
    target=Vector((x,0,z))
    cam.rotation_euler=(target-Vector(cam.location)).to_track_quat("-Z","Y").to_euler()
for loc,power,size in [((0,-5,7),900,6),((20,-4,6),850,5),((40,-4,7),1000,6),((60,-4,6),800,5),((80,-4,7),850,6)]:
    bpy.ops.object.light_add(type="AREA",location=loc)
    l=bpy.context.object; l.data.energy=power; l.data.shape="DISK"; l.data.size=size
    l.rotation_euler=(radians(25),0,0)

# Scene-by-scene character and camera blocking; each scene is ten seconds.
# 0-10: compulsive checking. 10-20: phone interrupts a real conversation.
# 20-30: attention splinters at work. 30-40: notification follows her outside.
# 40-50: she chooses to pause. 50-60: boundaries and calm.
for i,cx in enumerate(centers):
    start=1+i*240; end=start+239
    root.location=(cx,0,0)
    root.keyframe_insert(data_path="location",frame=start)
    root.keyframe_insert(data_path="location",frame=end)
    # Arm action: phone up at start, lower it during the boundary moment.
    for upper,fore,palm,side in arm_objs:
        upper.rotation_euler=(0,0,0); fore.rotation_euler=(0,0,0)
        upper.keyframe_insert(data_path="rotation_euler",frame=start)
        fore.keyframe_insert(data_path="rotation_euler",frame=start)
        # Reach/checking action in first four scenes; resting hand in final scenes.
        bend= -0.45 if side==1 and i<4 else 0.08
        upper.rotation_euler[1]=bend
        upper.keyframe_insert(data_path="rotation_euler",frame=start+65)
        fore.rotation_euler[1]=-.55 if i<4 else .10
        fore.keyframe_insert(data_path="rotation_euler",frame=start+65)
        upper.keyframe_insert(data_path="rotation_euler",frame=start+150)
        fore.keyframe_insert(data_path="rotation_euler",frame=start+150)
        if i>=4:
            upper.rotation_euler[1]=.25; fore.rotation_euler[1]=.15
            upper.keyframe_insert(data_path="rotation_euler",frame=end)
            fore.keyframe_insert(data_path="rotation_euler",frame=end)
    # Character settles and looks up as the story reaches its final scenes.
    head=bpy.data.objects.get("Mira head")
    if head:
        head.rotation_euler=(0,0,0); head.keyframe_insert(data_path="rotation_euler",frame=start)
        head.rotation_euler=(.04,0,.06 if i>=4 else -.05)
        head.keyframe_insert(data_path="rotation_euler",frame=start+180)
    # Camera starts wide, pushes in, then cuts to the next distinct set.
    for f,scale in [(start,9.0),(start+90,8.2),(start+210,8.2)]:
        cam.data.ortho_scale=scale; cam.data.keyframe_insert(data_path="ortho_scale",frame=f)
        aim(cx,1.65)
        cam.keyframe_insert(data_path="location",frame=f)
        cam.keyframe_insert(data_path="rotation_euler",frame=f)
# Smooth interpolation on camera and character, but preserve purposeful set-to-set cuts.
for ob in [root,cam,cam.data]+[x for pair in arm_objs for x in pair[:2]]:
    if ob.animation_data and ob.animation_data.action:
        for fc in ob.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation="BEZIER"
# Reapply camera keyframes as linear for a steady shot within each scene.
if cam.animation_data:
    for fc in cam.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation="LINEAR"

# Render a real 60-second sequence.
s.render.filepath=os.path.abspath(OUT+"/frame_")
s.render.image_settings.file_format="PNG"
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("renders/wise-lab-60sec-pilot.blend"))
bpy.ops.render.render(animation=True)
print("WISE_LAB_60_SECOND_PILOT_RENDER_COMPLETE")
