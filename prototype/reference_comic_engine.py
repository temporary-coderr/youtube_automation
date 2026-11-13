from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess

W,H,FPS=1280,720,24
DURATION=18
INK="#171923"; SKIN="#b8795b"; HOOD="#3a506b"
os.makedirs("renders",exist_ok=True)
try:
    FB=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",27)
    FM=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",21)
    FS=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",16)
except OSError: FB=FM=FS=ImageFont.load_default()
SCENES=[
 ("01  THE LOOP","You reach for your phone before the day even begins.","bedroom"),
 ("02  THE INTERRUPTION","One notification pulls your attention away.","street"),
 ("03  THE DISTRACTION","Minutes disappear while the world keeps moving.","bus"),
 ("04  THE RESET","You choose to put the phone down.","park")
]
def rr(d,b,c,o=INK,w=4,r=10): d.rounded_rectangle(b,radius=r,fill=c,outline=o,width=w)
def ln(d,p,c=INK,w=4): d.line(p,fill=c,width=w,joint="curve")
def poly(d,p,c,o=INK,w=4):
 d.polygon(p,fill=c)
 if o: d.line(p+[p[0]],fill=o,width=w,joint="curve")
def center(d,x,y,s,font=FM,c=INK):
 b=d.textbbox((0,0),s,font=font); d.text((x-(b[2]-b[0])/2,y),s,font=font,fill=c)
def bg(kind,t):
 im=Image.new("RGB",(W,H)); p=im.load()
 a=(25,42,61) if kind=="bedroom" else ((225,166,120) if kind=="street" else ((52,76,91) if kind=="bus" else (157,194,190)))
 b=(75,88,91) if kind=="bedroom" else ((65,76,88) if kind in ("street","bus") else (108,132,95))
 for y in range(H):
  q=y/(H-1); c=tuple(int(a[k]*(1-q)+b[k]*q) for k in range(3))
  for x in range(W): p[x,y]=c
 d=ImageDraw.Draw(im)
 if kind=="bedroom":
  rr(d,(55,65,440,350),"#263f55","#d8c7a6",8)
  d.ellipse((300,105,370,175),fill="#f2dca9")
  for i in range(26):
   x=(i*71-int(t*32))%330+80; y=(i*43)%220+90; ln(d,[(x,y),(x-7,y+16)],"#a7c2cc",2)
  poly(d,[(0,470),(1280,470),(1280,720),(0,720)],"#594a43",None)
  for y in (510,570,640): ln(d,[(0,y),(1280,y)],"#8c6c55",3)
  for x in range(-300,1600,220): ln(d,[(640,470),(x,720)],"#8c6c55",2)
  poly(d,[(430,360),(1120,360),(1200,420),(360,420)],"#9a6748")
  d.rectangle((405,420,455,660),fill="#503c35"); d.rectangle((1090,420,1140,660),fill="#503c35")
  rr(d,(560,245,840,355),"#202a38"); rr(d,(575,260,825,337),"#7895a0",None,0)
  center(d,700,280,"FOCUS",FS,"#f1e4c9")
  rr(d,(470,335,515,390),"#111923","#d4e4e8",3,7); d.rectangle((477,343,508,380),fill="#69a9c0")
  rr(d,(40,420,340,590),"#536779",INK,6,18); rr(d,(60,430,180,495),"#e6d9c5",INK,3,14)
 elif kind=="street":
  poly(d,[(0,330),(1280,330),(1280,720),(0,720)],"#404b58",None)
  for i in range(8):
   x=((i*210-int(t*95))%1550)-160; h=180+(i%3)*75
   poly(d,[(x,330-h),(x+165,330-h),(x+185,330),(x-10,330)],["#536b7c","#9b725b","#6a7f86"][i%3])
   for wx in range(x+22,x+145,48):
    for wy in range(350-h,300,62): rr(d,(wx,wy,wx+22,wy+30),"#f0d5a4",None,0,2)
  for y in (430,530,640):
   ln(d,[(640,330),(0,y)],"#d1b78e",3); ln(d,[(640,330),(1280,y)],"#d1b78e",3)
  for i in range(5):
   x=((i*310-int(t*180))%1500)-120
   rr(d,(x,430,x+55,560),"#263746",None,0,14); d.ellipse((x+8,395,x+48,435),fill="#263746")
  rr(d,(900,65,1190,145),"#f4e4c9"); center(d,1045,88,"ALWAYS ONLINE",FS)
 elif kind=="bus":
  rr(d,(35,35,1245,480),"#192c3d","#e8d8bd",8,20)
  for j,x in enumerate((65,355,645,935)):
   rr(d,(x,65,x+245,390),"#7795a0",INK,5,5)
   for i in range(4):
    bx=x+i*70-int(t*70)%70
    d.rectangle((bx,215-(i%2)*50,bx+48,390),fill=["#a8795c","#657b83","#b28d6d"][i%3])
   ln(d,[(x+120,65),(x+120,390)],"#d5c5a8",4)
  for x in (250,620,990):
   ln(d,[(x,0),(x,560)],"#d4b985",12); rr(d,(x-70,345,x+70,535),"#506677",INK,5,18)
  d.rectangle((0,545,W,720),fill="#4c5157")
  for x in range(0,W,180): ln(d,[(x,560),(x+90,560)],"#d8c39c",4)
 else:
  d.rectangle((0,420,W,H),fill="#71845f")
  for i in range(10):
   x=((i*175-int(t*24))%1500)-100; y=330+(i%3)*25
   d.rectangle((x-12,y,x+12,600),fill="#765744")
   d.ellipse((x-90,y-150,x+90,y+40),fill=["#557d69","#668b6e","#47715e"][i%3],outline=INK,width=3)
  poly(d,[(450,720),(610,425),(710,425),(950,720)],"#cbb58c",None)
  d.ellipse((970,55,1090,175),fill="#f5dfa2")
  rr(d,(790,455,1110,520),"#8b674b"); ln(d,[(820,510),(800,640)],"#594331",12); ln(d,[(1080,510),(1100,640)],"#594331",12)
 return im
def person(d,cx,base,s,pose,t,coat=HOOD,side=False):
 bob=math.sin(t*5)*2*s
 def P(x,y): return (int(cx+x*s),int(base+y*s+bob))
 d.ellipse((int(cx-75*s),int(base+3*s),int(cx+75*s),int(base+23*s)),fill="#28313a")
 if pose=="sit":
  ln(d,[P(-25,-130),P(-55,-55),P(-15,-35)],"#202a36",int(25*s)); ln(d,[P(25,-130),P(70,-65),P(105,-65)],"#202a36",int(25*s))
  rr(d,(int(cx-35*s),int(base-45*s),int(cx+12*s),int(base-24*s)),"#141d27",INK,2,7); rr(d,(int(cx+85*s),int(base-76*s),int(cx+135*s),int(base-54*s)),"#141d27",INK,2,7)
 else:
  ln(d,[P(-25,-130),P(-32,-65),P(-40,0)],"#202a36",int(27*s)); ln(d,[P(25,-130),P(34,-65),P(43,0)],"#202a36",int(27*s))
  rr(d,(int(cx-70*s),int(base-5*s),int(cx-20*s),int(base+18*s)),"#111a24",INK,2,7); rr(d,(int(cx+20*s),int(base-5*s),int(cx+76*s),int(base+18*s)),"#111a24",INK,2,7)
 poly(d,[P(-58,-300),P(55,-300),P(78,-135),P(-78,-135)],coat)
 ln(d,[P(-5,-290),P(-2,-205),P(12,-170)],"#73849a",max(2,int(3*s)))
 if pose=="phone":
  a1=[P(-48,-275),P(-88,-210),P(-58,-160)]; a2=[P(48,-275),P(85,-230),P(75,-190)]
 elif pose=="sit":
  a1=[P(-48,-275),P(-80,-210),P(-25,-175)]; a2=[P(48,-275),P(88,-220),P(35,-180)]
 else:
  a1=[P(-48,-275),P(-92,-215),P(-85,-150)]; a2=[P(48,-275),P(92,-215),P(95,-150)]
 for pts in (a1,a2):
  ln(d,pts,coat,max(12,int(25*s)))
  for q in pts[1:]: d.ellipse((q[0]-int(10*s),q[1]-int(10*s),q[0]+int(10*s),q[1]+int(10*s)),fill=SKIN,outline=INK,width=max(1,int(2*s)))
 rr(d,(int(cx-17*s),int(base-335*s),int(cx+18*s),int(base-290*s)),SKIN,INK,3,5)
 d.ellipse((int(cx-53*s),int(base-465*s+bob),int(cx+53*s),int(base-330*s+bob)),fill=SKIN,outline=INK,width=max(2,int(4*s)))
 d.ellipse((int(cx-62*s),int(base-410*s+bob),int(cx-38*s),int(base-370*s+bob)),fill=SKIN,outline=INK,width=2)
 poly(d,[(int(cx-57*s),int(base-410*s+bob)),(int(cx-53*s),int(base-465*s+bob)),(int(cx-20*s),int(base-445*s+bob)),(int(cx+2*s),int(base-478*s+bob)),(int(cx+24*s),int(base-445*s+bob)),(int(cx+55*s),int(base-460*s+bob)),(int(cx+60*s),int(base-395*s+bob))],"#17191f")
 ex=cx+(12 if side else -20)*s
 d.ellipse((int(ex-4*s),int(base-410*s+bob),int(ex+4*s),int(base-402*s+bob)),fill=INK); d.ellipse((int(cx+22*s),int(base-410*s+bob),int(cx+30*s),int(base-402*s+bob)),fill=INK)
 ln(d,[(int(cx-8*s),int(base-380*s+bob)),(int(cx+18*s),int(base-377*s+bob))],"#75473a",max(1,int(2*s)))
 if pose=="phone":
  px,py=P(85,-195); rr(d,(px-10,py-28,px+12,py+28),"#101923","#dce9e9",2,5); d.rectangle((px-6,py-21,px+8,py+18),fill="#6db5ca"); d.ellipse((px+3,py-34,px+14,py-23),fill="#f15f58")
def bubble(d,box,text,tail="left"):
 rr(d,box,"#fff8e9",INK,5,20); x1,y1,x2,y2=box
 pts=[(x1+55,y2-4),(x1+30,y2+30),(x1+95,y2-4)] if tail=="left" else [(x2-90,y2-4),(x2-35,y2+30),(x2-55,y2-4)]
 poly(d,pts,"#fff8e9",INK,4)
 words=text.split(); rows=[]; row=""
 for w in words:
  test=(row+" "+w).strip()
  if len(test)>29: rows.append(row); row=w
  else: row=test
 if row: rows.append(row)
 for i,s in enumerate(rows[:2]): center(d,(x1+x2)//2,y1+17+i*29,s,FM)
def render(t,idx,local):
 kind=SCENES[idx][2]; im=bg(kind,t); d=ImageDraw.Draw(im)
 # scrolling speed strokes establish constant movement behind the foreground
 for k in range(12):
  x=(k*137-int(t*45))%W; ln(d,[(x,480),(x-28,510)],"#e7d6b5",2)
 if idx==0:
  rr(d,(95,70,1185,620),"#e9dfcf",INK,10,5); person(d,360,585,1.05,"neutral",t)
  rr(d,(760,405,830,505),"#111923","#dce9e9",5,12); d.rectangle((770,420,820,485),fill="#65abc2")
  bubble(d,(560,105,1090,205),"Just ten more minutes...","right")
 elif idx==1:
  rr(d,(450,55,1195,625),"#f3e7d3",INK,10,5); person(d,820,610,1.65,"phone",t,side=True)
  for a in range(0,360,45):
   q=math.radians(a); ln(d,[(1040+math.cos(q)*45,280+math.sin(q)*45),(1040+math.cos(q)*78,280+math.sin(q)*78)],"#f4d06f",5)
  bubble(d,(70,95,470,215),"What's that sound?","right")
 elif idx==2:
  rr(d,(55,75,615,625),"#f4e8d5",INK,9,5); rr(d,(665,75,1225,625),"#f4e8d5",INK,9,5)
  person(d,335,595,1.05,"phone",t,side=True); person(d,945,595,1.05,"sit",t,coat="#8a594f")
  bubble(d,(700,105,1165,205),"You said you were listening.","left")
 else:
  rr(d,(80,60,1200,625),"#f4ead8",INK,10,5); person(d,440,600,1.45,"neutral",t)
  rr(d,(820,435,900,495),"#111923","#dce9e9",4,9); d.rectangle((829,444,891,483),fill="#4e8497")
  bubble(d,(660,100,1120,205),"Not every moment needs a screen.","left")
 rr(d,(30,22,365,70),"#f8edda",INK,4,8); d.text((48,35),SCENES[idx][0],font=FS,fill=INK)
 rr(d,(55,640,1225,700),"#182333","#f2e5cd",4,10)
 words=SCENES[idx][1].split(); x=82
 for i,w in enumerate(words):
  token=w+" "; d.text((x,657),token,font=FM,fill="#ffe27b" if i>=len(words)-3 else "#fff4df")
  x+=d.textbbox((0,0),token,font=FM)[2]
 return im
def main():
 narration=" ".join(s[1] for s in SCENES); wav="renders/reference-narration.wav"
 subprocess.run(["espeak-ng","-v","en-us","-s","145","-w",wav,narration],check=True)
 proc=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,"-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","renders/wise-lab-reference-style-18sec.mp4"],stdin=subprocess.PIPE)
 for f in range(DURATION*FPS):
  t=f/FPS; idx=min(3,int(t/(DURATION/4))); local=(t-idx*(DURATION/4))/(DURATION/4)
  frame=render(t,idx,local); zoom=1+0.025*local; cw,ch=int(W/zoom),int(H/zoom)
  px=int((W-cw)*([.2,.65,.4,.55][idx])); py=int((H-ch)*.45)
  frame=frame.crop((px,py,px+cw,py+ch)).resize((W,H),Image.Resampling.LANCZOS)
  if local<.08 and idx>0: frame=Image.blend(frame,Image.new("RGB",(W,H),"white"),.35*(1-local/.08))
  proc.stdin.write(frame.tobytes())
 proc.stdin.close(); code=proc.wait()
 if code: raise RuntimeError(f"ffmpeg exited {code}")
 print(f"Rendered {DURATION*FPS} frames, four reference-style comic beats")
if __name__=="__main__": main()
