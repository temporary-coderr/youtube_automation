#!/usr/bin/env python3
"""WISE-LAB cinematic 2D test: layered vector character, continuous action, camera moves, captions and narration."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, subprocess, wave
W,H,FPS=1280,720,24
OUT="renders/wise-lab-cinematic-2d.mp4"
os.makedirs("renders",exist_ok=True)
try:
    FONT=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",25)
    BOLD=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",29)
    SMALL=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",17)
except OSError: FONT=BOLD=SMALL=ImageFont.load_default()
INK="#171b25"; SKIN="#b97859"; HOOD="#34465b"; DARK="#202a38"; PANTS="#202b3b"; WOOD="#80583f"
LINES=[
("You finally sit down, ready to focus.","You finally sit down, ready to focus."),
("The room is quiet. Your attention is steady.","The room is quiet. Your attention is steady."),
("Then a notification flashes across your phone.","Then a notification flashes across your phone."),
("Before you decide, your hand is already moving.","Before you decide, your hand is already moving."),
("One small interruption pulls you out of the moment.","One small interruption pulls you out of the moment.")
]
def smooth(x):
 x=max(0,min(1,x)); return x*x*(3-2*x)
def line(d,p,c,w): d.line([(int(x),int(y)) for x,y in p],fill=c,width=max(1,int(w)),joint="curve")
def poly(d,p,c,o=INK,w=3):
 pts=[(int(x),int(y)) for x,y in p]; d.polygon(pts,fill=c)
 if o: d.line(pts+[pts[0]],fill=o,width=w,joint="curve")
def rr(d,b,r,c,o=INK,w=3): d.rounded_rectangle(tuple(map(int,b)),radius=int(r),fill=c,outline=o,width=w)
def ellipse(d,b,c,o=INK,w=2): d.ellipse(tuple(map(int,b)),fill=c,outline=o,width=w)
def gradient(top,bottom):
 a=Image.new("RGB",(1,H)); p=a.load()
 for y in range(H):
  t=y/(H-1); p[0,y]=tuple(int(int(top[i:i+2],16)*(1-t)+int(bottom[i:i+2],16)*t) for i in (1,3,5))
 return a.resize((W,H))
def room(t,scene):
 im=gradient("#1c2a40" if scene<2 else "#26394a","#59616a" if scene<2 else "#68706d")
 d=ImageDraw.Draw(im)
 # distant rainy window, trim and moving rain streaks
 rr(d,(55,55,425,365),8,"#101c30","#d9c7a5",9); rr(d,(70,70,410,350),3,"#354f68",None,0)
 ellipse(d,(315,95,370,150),"#f3dba8",None,0)
 for k in range(32):
  x=82+(k*71+int(t*63))%310; y=82+(k*43+int(t*105))%245
  line(d,[(x,y),(x-9,y+20)],"#91aabd",2)
 line(d,[(240,70),(240,352)],"#d7c5a4",7); line(d,[(70,210),(410,210)],"#d7c5a4",7)
 # wall framed art, shelf, books and plant
 rr(d,(760,75,1005,235),5,"#dfd2bc",INK,5); rr(d,(774,89,991,220),3,"#6d8791",None,0)
 poly(d,[(774,220),(860,130),(925,220)],"#3c5961",None); ellipse(d,(925,105,960,140),"#f2d69c",None,0)
 rr(d,(1040,120,1210,137),4,WOOD,INK,3)
 for x,c,h in [(1060,"#ad7656",70),(1094,"#526c79",88),(1130,"#b69a70",61),(1163,"#536c5b",80)]:
  rr(d,(x,137-h,x+23,137),2,c,INK,2)
 # floorboards and rug
 poly(d,[(0,485),(1280,465),(1280,720),(0,720)],"#303a43",None)
 for y in (540,610,680): line(d,[(0,y),(1280,y-18)],"#4b5359",2)
 poly(d,[(130,650),(950,590),(1190,720),(0,720)],"#45525b",None)
 # desk with perspective legs, drawers
 poly(d,[(480,405),(1195,405),(1250,452),(450,452)],"#a87550",INK,5)
 poly(d,[(470,450),(515,450),(510,675),(475,675)],"#604432",INK,4)
 poly(d,[(1150,450),(1190,450),(1200,660),(1160,660)],"#604432",INK,4)
 rr(d,(735,421,920,444),3,"#e6ddc9",INK,2)
 for y in (428,435): line(d,[(750,y),(900,y)],"#a8a59b",2)
 # laptop and screen
 rr(d,(930,320,1105,410),8,"#1b2634","#9daeb7",4); rr(d,(941,331,1094,397),3,"#526d7c",None,0)
 rr(d,(910,408,1120,420),5,"#b8c0bf",INK,2)
 # phone, cup, pencil, lamp, potted plant
 rr(d,(605,410,653,448),7,"#121a26","#c6d3d6",3); rr(d,(611,416,647,439),3,"#6db4c5",None,0)
 rr(d,(680,410,725,454),8,"#e5e0d3",INK,3); ellipse(d,(714,420,737,444),"#e5e0d3",INK,3)
 line(d,[(765,410),(815,390)],"#d9b66d",6)
 ellipse(d,(1130,420,1190,455),"#c28d5f",INK,3)
 for k in range(5):
  x=1160+(k-2)*17; line(d,[(1160,420),(x,370-(k%2)*20)],"#658a6d",8)
 # lamp with animated warm glow
 ellipse(d,(500,380,670,520),(70,80,88),None,0)
 line(d,[(540,415),(560,300),(610,270)],"#c9b78e",13)
 poly(d,[(570,245),(665,245),(640,295),(590,295)],"#e6cc91",INK,4)
 return im
def character(d,t,x,base,walk=0,reach=0,scale=1.0):
 # local coordinates helper, character height ~480px
 def P(a,b): return (x+a*scale,base+b*scale)
 bob=math.sin(t*10)*4*walk
 # chair silhouette behind seated character
 rr(d,(x-98*scale,base-265*scale,x+92*scale,base-10*scale),20*scale,"#435467",INK,5)
 line(d,[P(-75,-10),P(-85,25)],"#252f3b",12*scale); line(d,[P(70,-10),P(82,25)],"#252f3b",12*scale)
 # legs with alternating stride / seated bent position
 stride=math.sin(t*7)*28*walk
 hip=P(-2,-150+bob)
 if walk>0.2:
  knee1=P(-38+stride,-78); ankle1=P(-48+stride*1.3,-8)
  knee2=P(38-stride,-83); ankle2=P(48-stride*1.3,-8)
 else:
  knee1=P(-68,-75); ankle1=P(-112,-15); knee2=P(82,-72); ankle2=P(128,-12)
 line(d,[hip,knee1,ankle1],PANTS,38*scale); line(d,[hip,knee1,ankle1],"#111923",2*scale)
 line(d,[hip,knee2,ankle2],PANTS,38*scale); line(d,[hip,knee2,ankle2],"#111923",2*scale)
 for a,b in (ankle1,ankle2):
  rr(d,(a-38*scale,b-7*scale,a+23*scale,b+20*scale),12*scale,"#151d29","#0c111a",3)
  line(d,[(a-23*scale,b+3*scale),(a+10*scale,b+3*scale)],"#aeb8bd",2*scale)
 # torso hoodie with hood, seams, pocket, drawstrings
 top=P(-78,-365+bob); bot=P(82,-145+bob)
 poly(d,[P(-55,-365+bob),P(50,-365+bob),P(83,-160+bob),P(-82,-160+bob)],HOOD,INK,5*scale)
 poly(d,[P(-55,-350+bob),P(-30,-395+bob),P(30,-395+bob),P(58,-350+bob)],"#26364a",INK,4*scale)
 line(d,[P(-6,-355+bob),P(-2,-265+bob)],"#718196",3*scale)
 line(d,[P(12,-355+bob),P(8,-265+bob)],"#718196",3*scale)
 rr(d,(x-43*scale,base-242*scale+bob,x+42*scale,base-190*scale+bob),9*scale,"#2b3a4c","#1a2634",2)
 # hoodie folds
 for off in (-48,45):
  line(d,[P(off,-330+bob),P(off*0.7,-275+bob),P(off*0.55,-230+bob)],"#596a7d",2*scale)
 # neck and head
 rr(d,(x-20*scale,base-410*scale+bob,x+22*scale,base-355*scale+bob),8*scale,SKIN,INK,3)
 ellipse(d,(x-59*scale,base-505*scale+bob,x+59*scale,base-380*scale+bob),SKIN,INK,4*scale)
 ellipse(d,(x-67*scale,base-457*scale+bob,x-45*scale,base-415*scale+bob),SKIN,INK,3)
 ellipse(d,(x+45*scale,base-457*scale+bob,x+67*scale,base-415*scale+bob),SKIN,INK,3)
 # hair cap and individually defined locks
 poly(d,[P(-61,-445+bob),P(-58,-492+bob),P(-30,-518+bob),P(-13,-493+bob),P(8,-525+bob),P(24,-493+bob),P(56,-504+bob),P(63,-445+bob),P(38,-455+bob),P(15,-467+bob),P(-8,-450+bob)],"#17191f",INK,3*scale)
 # eyebrows, eyes, nose, mouth, ear highlight
 for ex in (-22,23):
  line(d,[P(ex-9,-454+bob),P(ex+7,-457+bob)],"#392a28",3*scale)
  ellipse(d,(x+(ex-3)*scale,base-448*scale+bob,x+(ex+4)*scale,base-441*scale+bob),"#17191f",None,0)
 line(d,[P(1,-445+bob),P(-3,-424+bob),P(5,-421+bob)],"#8e5d49",2*scale)
 line(d,[P(-10,-404+bob),P(8,-402+bob)],"#6d3e37",2*scale)
 # arms as two-segment articulated limbs; right reaches phone in later beat
 shL=P(-62,-340+bob); elL=P(-112,-270+bob); wrL=P(-75,-220+bob)
 shR=P(62,-340+bob)
 elbow=(x+(110+35*reach)*scale,base+(-260+5*reach)*scale+bob)
 wrist=(x+(150+65*reach)*scale,base+(-215+12*reach)*scale+bob)
 line(d,[shL,elL,wrL],HOOD,31*scale); ellipse(d,(elL[0]-13*scale,elL[1]-13*scale,elL[0]+13*scale,elL[1]+13*scale),HOOD,INK,2)
 line(d,[shR,elbow,wrist],HOOD,32*scale); ellipse(d,(elbow[0]-15*scale,elbow[1]-15*scale,elbow[0]+15*scale,elbow[1]+15*scale),HOOD,INK,2)
 # hands and separated fingers
 for px,py in (wrL,wrist):
  ellipse(d,(px-13*scale,py-12*scale,px+14*scale,py+13*scale),SKIN,INK,2)
  for j in range(3): line(d,[(px+7*scale,py+(j-1)*5*scale),(px+17*scale,py+(j-1)*6*scale)],SKIN,3*scale)
def frame(t):
 # 5 beats over 20 sec; same action in a continuous bedroom set, reframed with camera pushes
 beat=min(4,int(t/4)); u=(t-beat*4)/4
 im=room(t,beat); d=ImageDraw.Draw(im)
 if beat==0:
  character(d,t,230+360*smooth(u),650,walk=1-smooth((u-.7)/.3),reach=0,scale=.78)
 elif beat==1:
  character(d,t,610,650,walk=0,reach=0,scale=1.0)
 elif beat==2:
  character(d,t,610,650,walk=0,reach=0,scale=1.0)
  # screen notification pulse, expanding ring and floating alert
  pulse=1+0.15*math.sin(t*9); ellipse(d,(616-23*pulse,430-23*pulse,616+23*pulse,430+23*pulse),None,"#ffe17b",4)
  ellipse(d,(625,394,648,417),"#ed655c",INK,2); d.text((631,394),"1",font=SMALL,fill="white")
 elif beat==3:
  r=smooth(u); character(d,t,610,650,walk=0,reach=r,scale=1.0)
  # hand motion streaks
  for j in range(3): line(d,[(790+j*12,430-j*8),(805+j*12,420-j*8)],"#f5d27c",3)
 else:
  character(d,t,610,650,walk=0,reach=1,scale=1.0)
  # phone lifts and tilts into the hand, screen scroll streaks
  lift=smooth(u); px=770+lift*38; py=427-lift*90
  rr(d,(px-20,py-38,px+20,py+38),7,"#111a26","#c4d2d8",3)
  rr(d,(px-15,py-29,px+15,py+27),4,"#65afc5",None,0)
  for j in range(3): line(d,[(px-9,py-16+j*12),(px+9,py-16+j*12)],"#e4f1e8",2)
 # gentle camera crop/pan, distinct framing for every beat
 zoom=[1.0,1.035,1.07,1.09,1.13][beat]
 cw,ch=int(W/zoom),int(H/zoom)
 panx=int((W-cw)*([.08,.35,.43,.5,.57][beat])); pany=int((H-ch)*.46)
 im=im.crop((panx,pany,panx+cw,pany+ch)).resize((W,H),Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im)
 # title slug and precise narration caption strip
 rr(d,(34,24,380,70),10,"#111a29","#d9c9a9",2)
 d.text((52,37),"WISE-LAB  /  ATTENTION",font=SMALL,fill="#f5e8d0")
 caption=LINES[beat][0]
 rr(d,(48,594,1232,686),14,"#111a29","#e7d6b5",3)
 box=d.textbbox((0,0),caption,font=BOLD); d.text(((W-(box[2]-box[0]))/2,620),caption,font=BOLD,fill="#fff3dc")
 return im
def main():
 wav="renders/wise-lab-narration.wav"
 narration=" ".join(x[1] for x in LINES)
 subprocess.run(["espeak-ng","-v","en-us","-s","145","-w",wav,narration],check=True)
 with wave.open(wav,"rb") as f: duration=f.getnframes()/f.getframerate()
 duration=min(duration,20.0); total=math.ceil(duration*FPS)
 # Keep the five action beats evenly aligned to narration duration.
 proc=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,"-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",OUT],stdin=subprocess.PIPE)
 for i in range(total):
  t=i/FPS*20/max(duration,.01)
  proc.stdin.write(frame(t).tobytes())
 proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError("ffmpeg failed")
 # SRT sidecar: one caption per narrated beat.
 with open("renders/wise-lab-cinematic-2d.srt","w",encoding="utf-8") as f:
  for i,(cap,_) in enumerate(LINES):
   a=i*duration/5; b=(i+1)*duration/5
   def stamp(v):
    ms=int(v*1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
   f.write(f"{i+1}\n{stamp(a)} --> {stamp(b)}\n{cap}\n\n")
 print(f"Rendered {total} frames at {W}x{H}; {duration:.2f}s narration; SRT created.")
if __name__=="__main__": main()
