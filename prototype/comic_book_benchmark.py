from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess, wave
W,H,FPS=1280,720,24
OUT="renders/comic"; os.makedirs(OUT,exist_ok=True)
try:
 title=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",42)
 capfont=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",29)
 small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",20)
except OSError: title=capfont=small=ImageFont.load_default()
def poly(d,p,c):
 d.polygon(p,fill=c); d.line(p+[p[0]],fill="#10131c",width=6,joint="curve")
def scene(n,t):
 im=Image.new("RGB",(W,H),"#10131c"); d=ImageDraw.Draw(im)
 d.rectangle((18,18,1262,702),fill="#26384c" if n!=1 else "#18283a",outline="#f5e7cf",width=7)
 for y in range(42,690,22):
  for x in range(42,1240,22):
   if (x//22+y//22)%3==0: d.ellipse((x,y,x+2,y+2),fill="#526174")
 d.rounded_rectangle((75,75,390,365),radius=8,fill="#0d1a31",outline="#e8d8b8",width=12)
 d.ellipse((285,110,335,160),fill="#f5dfa6"); d.line((232,80,232,360),fill="#e8d8b8",width=8); d.line((80,220,385,220),fill="#e8d8b8",width=8)
 d.rectangle((470,475,1190,515),fill="#9a6243",outline="#17151a",width=7); d.rectangle((520,515,555,675),fill="#543a30"); d.rectangle((1110,515,1145,675),fill="#543a30")
 d.polygon([(690,360),(1010,360),(1040,470),(665,470)],fill="#202b38",outline="#080d14")
 d.rectangle((720,380,985,450),fill="#6da6b5",outline="#080d14",width=5); d.line((750,402,950,402),fill="#d5e9e4",width=4); d.line((750,420,900,420),fill="#d5e9e4",width=4)
 d.rectangle((1040,440,1150,468),fill="#eee0c2",outline="#17151a",width=4); d.ellipse((1130,420,1190,480),fill="#e9e0ce",outline="#17151a",width=5)
 d.rounded_rectangle((520,425,590,470),radius=8,fill="#111723",outline="#a8c5d0",width=4); d.rectangle((528,431,582,462),fill="#172d42")
 if n>=1:
  glow=int(120+100*(.5+.5*math.sin(t*9))); d.rounded_rectangle((530,438,580,455),radius=4,fill=(25,glow,min(255,glow+35))); d.ellipse((574,427,588,441),fill="#ff5b56",outline="#10131c",width=2)
 d.rounded_rectangle((300,390,470,635),radius=35,fill="#35475a",outline="#111722",width=7)
 poly(d,[(365,500),(425,500),(470,620),(425,640),(370,555)],"#202a38"); poly(d,[(420,610),(490,620),(500,650),(420,650)],"#151b24")
 poly(d,[(315,255),(430,255),(480,455),(300,455)],"#343c4b")
 d.rectangle((355,225,400,275),fill="#9b674f",outline="#17131a",width=4); d.ellipse((320,105,435,250),fill="#a96f53",outline="#17131a",width=6)
 d.pieslice((310,85,445,225),180,355,fill="#17191f",outline="#11131a",width=4)
 d.polygon([(320,150),(335,100),(360,125),(380,95),(405,125),(435,105),(440,165)],fill="#17191f",outline="#11131a")
 if n==0: poly(d,[(325,285),(350,290),(430,390),(410,410)],"#343c4b"); d.ellipse((405,390,440,425),fill="#a96f53",outline="#17131a",width=4)
 else: poly(d,[(410,285),(445,290),(620,440),(595,465)],"#343c4b"); d.ellipse((590,440,625,475),fill="#a96f53",outline="#17131a",width=4)
 if n==1: d.text((590,300),"!",font=title,fill="#ffe16d",stroke_width=3,stroke_fill="#14151b")
 if n==2:
  d.text((530,330),"BZZT!",font=title,fill="#ffe16d",stroke_width=4,stroke_fill="#14151b")
  for k in range(3): d.arc((495-k*12,405-k*12,620+k*12,500+k*12),195,335,fill="#9bd8e2",width=3)
 labels=["01  FOCUS","02  INTERRUPTION","03  ATTENTION SHIFT"]
 d.rounded_rectangle((48,38,420,92),radius=10,fill="#f4e6ca",outline="#11131a",width=4); d.text((66,49),labels[n],font=small,fill="#17202b")
 return im
def wrap(d,s,font,maxw):
 lines=[]; line=""
 for word in s.split():
  test=(line+" "+word).strip()
  if d.textbbox((0,0),test,font=font)[2]<=maxw: line=test
  else:
   if line: lines.append(line)
   line=word
 if line: lines.append(line)
 return lines
def main():
 wav=OUT+"/narration.wav"
 with wave.open(wav,"rb") as wf: dur=wf.getnframes()/wf.getframerate()
 dur=max(12.0,dur); total=math.ceil(dur*FPS)
 caps=[(0,dur*.34,"Your attention feels like it's under your control."),(dur*.34,dur*.68,"Then one small notification breaks your focus."),(dur*.68,dur,"And suddenly, your mind is somewhere else.")]
 for f in range(total):
  t=f/FPS; n=0 if t<dur*.34 else (1 if t<dur*.68 else 2); local=t-(0 if n==0 else dur*.34 if n==1 else dur*.68)
  im=scene(n,t); zoom=1+.055*min(1,local/max(.1,dur/3)); cw,ch=int(W/zoom),int(H/zoom); left=int((W-cw)*(.25+.5*local/max(.1,dur/3))); top=int((H-ch)*.35)
  im=im.crop((left,top,left+cw,top+ch)).resize((W,H),Image.Resampling.LANCZOS); d=ImageDraw.Draw(im)
  caption=next((s for a,b,s in caps if a<=t<b),caps[-1][2])
  d.rounded_rectangle((70,570,1210,680),radius=18,fill="#111722",outline="#f4e6ca",width=4)
  for i,line in enumerate(wrap(d,caption,capfont,1060)[:2]):
   tw=d.textbbox((0,0),line,font=capfont)[2]; d.text(((W-tw)//2,588+i*36),line,font=capfont,fill="#fff3dc",stroke_width=1,stroke_fill="#111722")
  if f in (int(dur*FPS*.34),int(dur*FPS*.68)): im=Image.blend(im,Image.new("RGB",(W,H),"#fff0c8"),.13)
  im.save(f"{OUT}/frame_{f+1:04d}.jpg",quality=91)
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),"-i",f"{OUT}/frame_%04d.jpg","-i",wav,"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","renders/wise-lab-comic-20sec.mp4"],check=True)
 print("Rendered",total,"comic frames; narration",round(dur,2),"seconds")
if __name__=="__main__": main()
