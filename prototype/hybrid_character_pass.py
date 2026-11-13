import bpy, math, os
from mathutils import Vector
from math import radians
# Transparent Blender character pass; backgrounds/props are supplied as an illustrated frame.
OUT="renders/character"; os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
s=bpy.context.scene; s.render.engine="BLENDER_EEVEE"; s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100
s.render.fps=24; s.frame_start=1; s.frame_end=168; s.eevee.taa_render_samples=8
s.render.image_settings.file_format="PNG"; s.render.image_settings.color_mode="RGBA"; s.render.film_transparent=True
s.view_settings.view_transform="Standard"; s.view_settings.look="Medium High Contrast"
def material(n,c):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*c,1); m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value=.78; return m
skin=material("warm skin",(.58,.34,.25)); hoodie=material("charcoal hoodie",(.075,.095,.13)); pants=material("black jeans",(.025,.035,.055)); hair=material("black hair",(.018,.022,.03)); shoes=material("sneakers",(.08,.09,.11)); white=material("eye whites",(.9,.88,.82))
def ellipsoid(name,loc,scale,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(mat); bpy.ops.object.shade_smooth(); return o
def capsule(name,a,b,r,mat):
 a=Vector(a); b=Vector(b); d=b-a; mid=(a+b)/2
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d.length,location=mid); o=bpy.context.object; o.name=name; o.rotation_mode="QUATERNION"; o.rotation_quaternion=d.to_track_quat("Z","Y"); o.data.materials.append(mat)
 bevel=o.modifiers.new("soft ends","BEVEL"); bevel.width=r*.9; bevel.segments=4; o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
 # Add rounded joints at both ends
 ellipsoid(name+" joint A",a,(r,r,r),mat); ellipsoid(name+" joint B",b,(r,r,r),mat)
 return o
# Orthographic front camera, character occupies ~62% of frame height.
bpy.ops.object.camera_add(location=(0,-12,2.6)); cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.ortho_scale=9.6; cam.rotation_euler=(radians(90),0,0); s.camera=cam
# Character local coordinates, facing camera. Root travels toward desk; head/torso stay connected.
root=bpy.data.objects.new("character_root",None); bpy.context.collection.objects.link(root)
# Body and head
torso=ellipsoid("hoodie torso",(0,0,1.55),(.48,.27,.66),hoodie); head=ellipsoid("head",(0,-.015,2.42),(.32,.29,.39),skin)
haircap=ellipsoid("messy hair",(0,.015,2.68),(.34,.30,.22),hair)
# face points toward camera (-Y)
for x in (-.12,.12): ellipsoid("eye",(x,-.292,2.46),(.035,.018,.045),white)
# hoodie pocket and drawstrings
pocket=ellipsoid("hoodie pocket",(0,-.265,1.35),(.27,.025,.12),hoodie)
# limbs as separate articulated sections with pivot empties and child geometry
def limb_segment(name,pivot,vec,r,mat):
 # geometry centered from pivot to pivot+vec; local mesh coordinates around pivot
 length=Vector(vec).length
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=length,location=Vector(pivot)+Vector(vec)/2)
 o=bpy.context.object; o.name=name; o.rotation_mode="QUATERNION"; o.rotation_quaternion=Vector(vec).to_track_quat("Z","Y"); o.data.materials.append(mat)
 be=o.modifiers.new("rounded ends","BEVEL"); be.width=r*.85; be.segments=4; o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
 return o
# For this first hybrid proof, animate limb segments with keyframed endpoint positions, avoiding broken bone-parent transforms.
parts=[]
def link_part(obj):
 obj.parent=root; parts.append(obj); return obj
for ob in (torso,head,haircap,pocket): link_part(ob)
# limbs built from capsules; endpoint coordinates are updated by frame handler below
def make_limb(name,a,b,r,mat):
 ob=limb_segment(name,a,Vector(b)-Vector(a),r,mat); link_part(ob); return ob
upperL=make_limb("left upper arm",(-.37,0,1.92),(-.62,0,1.48),.14,hoodie)
foreL=make_limb("left forearm",(-.62,0,1.48),(-.58,-.01,1.08),.115,hoodie)
upperR=make_limb("right upper arm",(.37,0,1.92),(.62,0,1.48),.14,hoodie)
foreR=make_limb("right forearm",(.62,0,1.48),(.58,-.01,1.08),.115,hoodie)
thighL=make_limb("left thigh",(-.19,0,1.05),(-.23,0,.55),.17,pants)
shinL=make_limb("left shin",(-.23,0,.55),(-.23,-.02,.12),.13,pants)
thighR=make_limb("right thigh",(.19,0,1.05),(.23,0,.55),.17,pants)
shinR=make_limb("right shin",(.23,0,.55),(.23,-.02,.12),.13,pants)
for x in (-.23,.23): link_part(ellipsoid("sneaker",(x,-.08,.08),(.22,.31,.12),shoes))
# Parent all character pieces to root while retaining local positions.
for ob in parts:
 if ob.parent is not root:
  world=ob.matrix_world.copy(); ob.parent=root; ob.matrix_world=world
# Animate root approach and camera push-in.
for f,x in [(1,-1.5),(36,-.8),(72,-.25),(168,-.25)]:
 root.location.x=x; root.keyframe_insert(data_path="location",frame=f)
# Subtle walk gait by swinging legs/arms around each object's own origin; visual action phases.
for ob,axis,keys in [
 (thighL,"rotation_euler",[(1,(.25,0,0)),(18,(-.25,0,0)),(36,(.1,0,0)),(60,(0,0,0)),(168,(0,0,0))]),
 (thighR,"rotation_euler",[(1,(-.25,0,0)),(18,(.25,0,0)),(36,(-.1,0,0)),(60,(0,0,0)),(168,(0,0,0))]),
 (upperL,"rotation_euler",[(1,(-.2,0,0)),(18,(.2,0,0)),(36,(0,0,0)),(168,(0,0,0))]),
 (upperR,"rotation_euler",[(1,(.2,0,0)),(18,(-.2,0,0)),(36,(0,0,0)),(78,(-.65,0,0)),(110,(-.9,0,0)),(168,(-.9,0,0))]),
 (foreR,"rotation_euler",[(1,(0,0,0)),(78,(-.2,0,0)),(110,(-.45,0,0)),(168,(-.45,0,0))])]:
 for f,v in keys:
  ob.rotation_euler=v; ob.keyframe_insert(data_path=axis,frame=f)
# Soft lighting
for typ,loc,power,size in [("AREA",(-3,-4,6),650,5),("AREA",(3,1,4),350,4)]:
 bpy.ops.object.light_add(type=typ,location=loc); l=bpy.context.object; l.data.energy=power; l.data.shape="DISK"; l.data.size=size; l.rotation_euler=(radians(25),0,radians(20))
s.render.filepath=os.path.abspath(OUT+"/frame_"); s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("renders/hybrid-character.blend"))
bpy.ops.render.render(animation=True)
print("HYBRID_CHARACTER_PASS_COMPLETE")
