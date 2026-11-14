#!/usr/bin/env python3
"""WISE-LAB articulated 2D character animation benchmark.
Procedural cut-out rig with 2-bone IK, planted gait phases and hand-parented prop.
"""
import math, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
W,H,FPS,SECONDS=1280,720,24,12
OUT="renders/2d-rig-benchmark.mp4"; DIR="renders/2d-rig-frames"
os.makedirs(DIR,exist_ok=True)

def clamp(v,a,b): return max(a,min(b,v))
def smooth(t):
 t=clamp(t,0,1); return t*t*(3-2*t)
def mix(a,b,t): return a+(b-a)*t
def pt(a,b,t): return (mix(a[0],b[0],t),mix(a[1],b[1],t))
def ellipse(d,p,r,fill,outline=None,w=1):
 x,y=p; d.ellipse((int(x-r),int(y-r),int(x+r),int(y+r)),fill=fill,outline=outline,width=w)
def segment(d,a,b,width,color,edge=(27,29,36)):
 d.line((a,b),fill=edge,width=width+5)
 d.line((a,b),fill=color,width=width)
 ellipse(d,a,width/2,color,edge,2); ellipse(d,b,width/2,color,edge,2)
def rounded(d,box,r,fill,outline=None,w=1):
 d.rounded_rectangle(tuple(map(int,box)),radius=r,fill=fill,outline=outline,width=w)

def ik(a,c,l1,l2,bend=1):
 dx,dy=c[0]-a[0],c[1]-a[1]; dist=max(1,math.hypot(dx,dy))
 dist=clamp(dist,abs(l1-l2)+.01,l1+l2-.01)
 along=(l1*l1-l2*l2+dist*dist)/(2*dist)
 h=math.sqrt(max(0,l1*l1-along*along))
 ux,uy=dx/dist,dy/dist
 return (a[0]+ux*along-bend*uy*h,a[1]+uy*along+bend*ux*h)

def background():
 im=Image.new("RGB",(W,H)); p=im.load()
 for y in range(H):
  c=(int(20+13*y/H),int(29+11*y/H),int(48+9*y/H))
  for x in range(W): p[x,y]=c
 d=ImageDraw.Draw(im)
 rounded(d,(28,25,510,390),15,(24,45,66),(86,103,120),7)
 for x,h in [(50,110),(112,165),(180,125),(245,190),(320,145),(390,172),(450,112)]:
  rounded(d,(x,360-h,x+38,360),2,(17,29,46))
  for yy in range(360-h+15,350,27):
   for xx in range(x+8,x+35,14): rounded(d,(xx,yy,xx+5,yy+8),1,(192,155,101))
 d.line([(269,25),(269,390)],fill=(83,99,116),width=6)
 d.line([(28,205),(510,205)],fill=(83,99,116),width=6)
 d.rectangle((0,420,W,H),fill=(48,42,48)); d.line((0,420,W,420),fill=(112,86,71),width=8)
 for y in range(480,720,70): d.line((0,y,W,y),fill=(62,54,57),width=2)
 rounded(d,(600,420,1200,458),8,(105,70,54),(153,112,83),3)
 rounded(d,(650,455,680,690),6,(60,48,44)); rounded(d,(1140,455,1170,690),6,(60,48,44))
 rounded(d,(770,390,950,417),5,(220,208,180),(244,230,202),2)
 d.line((790,397,930,397),fill=(151,138,119),width=2)
 # lamp
 d.line((1090,420,1090,310,1050,270),fill=(47,50,57),width=12)
 ellipse(d,(1050,270),30,(197,151,90))
 return im

def draw_phone(d,center,scale=1):
 x,y=center; w,h=19*scale,36*scale
 rounded(d,(x-w,y-h,x+w,y+h),7,(12,16,23),(150,163,176),3)
 rounded(d,(x-w+5,y-h+7,x+w-5,y+h-10),4,(68,132,172))
 ellipse(d,(x,y+h-5),2,(190,198,205))

def character(im,t,walk,reach,lift):
 d=ImageDraw.Draw(im)
 # Root travels only during first phase; pelvis/torso respond to gait and reach
 root_x=mix(285,420,walk)
 phase=t*2*math.pi*1.15
 bob=abs(math.sin(phase))*5*(1-walk*.9)
 hip=(root_x,535+bob); shoulder=(root_x+2,366+bob)
 # head/torso
 ellipse(d,(root_x,661),76,(22,23,29))
 # legs with alternating planted/swing foot targets, solved by knee IK
 for side in (-1,1):
  offset=0 if side==-1 else math.pi
  cyc=(phase+offset)%(2*math.pi)
  stance=cyc<math.pi
  u=cyc/math.pi if stance else (cyc-math.pi)/math.pi
  if walk<.98:
   if stance:
    foot=(root_x+side*20+(-18+36*u),650)
   else:
    foot=(root_x+side*20+(18-36*u),650-42*math.sin(math.pi*u))
  else:
   foot=(root_x+side*28,650)
  knee=ik((hip[0]+side*19,hip[1]),foot,76,78,bend=1 if side==1 else -1)
  upper=(45,48,60); lower=(31,34,43)
  segment(d,(hip[0]+side*19,hip[1]),knee,29,upper)
  segment(d,knee,foot,24,lower)
  # shoes
  rounded(d,(foot[0]-24,foot[1]-8,foot[0]+27,foot[1]+12),8,(15,18,25),(7,8,12),2)
 # torso silhouette
 ellipse(d,shoulder,56,(47,53,66),(82,88,100),3)
 rounded(d,(root_x-43,390+bob,root_x+45,535+bob),26,(48,54,67),(83,89,101),3)
 d.line((root_x,400+bob,root_x,510+bob),fill=(87,93,104),width=3)
 rounded(d,(root_x-31,478+bob,root_x+31,515+bob),9,(39,44,56),(79,84,96),2)
 # neck/head and hair
 rounded(d,(root_x-16,315+bob,root_x+17,370+bob),8,(151,104,79))
 ellipse(d,(root_x,274+bob),48,(164,116,88),(72,50,43),3)
 ellipse(d,(root_x,235+bob),48,(29,28,31))
 for dx,dy in [(-36,-35),(-18,-52),(5,-55),(27,-44),(42,-25)]:
  ellipse(d,(root_x+dx,274+bob+dy),19,(29,28,31))
 ellipse(d,(root_x+23,271+bob),3,(35,29,27))
 # relaxed left arm articulated
 ls=(root_x-43,390+bob); le=(root_x-79,444+bob); lh=(root_x-73,496+bob)
 segment(d,ls,le,25,(48,54,67)); segment(d,le,lh,21,(48,54,67)); ellipse(d,lh,12,(164,116,88))
 # right arm: target hand travels to phone; IK creates elbow bend
 rs=(root_x+42,390+bob)
 target=(mix(root_x+75,875,reach),mix(465,390,reach))
 elbow=ik(rs,target,72,74,bend=-1)
 segment(d,rs,elbow,27,(48,54,67)); segment(d,elbow,target,22,(48,54,67))
 ellipse(d,target,13,(164,116,88),(112,75,60),2)
 # fingers close around phone after contact
 if reach>.82:
  d.line((target[0]+4,target[1]-5,target[0]+17,target[1]+1),fill=(128,83,65),width=4)
 # Phone follows hand once grabbed; position remains on desk before grasp
 phone=(880,380)
 if lift>0: phone=(mix(880,target[0]+17,lift),mix(380,target[1]+2,lift))
 draw_phone(d,phone)
 return phone

def render(i):
 t=i/FPS
 walk=smooth((t-.5)/3.4)
 reach=smooth((t-4.1)/2.0)
 lift=smooth((t-7.0)/1.2)
 im=background()
 phone=character(im,t,walk,reach,lift)
 # glow around phone, light-touch camera vignette
 glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
 ellipse(gd,phone,42,(83,176,220,26))
 im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(20))).convert("RGB")
 d=ImageDraw.Draw(im)
 rounded(d,(52,54,420,112),14,(12,19,30)); d.text((78,72),"WISE-LAB  /  ARTICULATED 2D",fill=(215,222,231))
 return im

for i in range(SECONDS*FPS):
 render(i).save(f"{DIR}/{i:04d}.png",compress_level=1)
 if (i+1)%48==0: print(f"FRAMES {i+1}/{SECONDS*FPS}",flush=True)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{DIR}/%04d.png","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",OUT],check=True)
print("DONE",OUT)
