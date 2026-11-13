from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess

W,H,FPS,DURATION=1280,720,24,20
INK="#171923"; SKIN="#b8795b"; HOOD="#344b63"
os.makedirs("renders",exist_ok=True)
try:
    F_CAP=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",25)
    F_SMALL=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",17)
    F_TINY=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",13)
except OSError:
    F_CAP=F_SMALL=F_TINY=ImageFont.load_default()

SCENES=[
 ("01  THE HABIT","You reach for your phone before the day even begins.","bedroom"),
 ("02  THE INTERRUPTION","One notification pulls your attention away.","bedroom_close"),
 ("03  THE DISTRACTION","Minutes disappear while the world keeps moving.","bus"),
 ("04  THE RESET","You choose to put the phone down.","park")
]
def clamp(v,a=0,b=1): return max(a,min(b,v))
def ease(v):
    v=clamp(v); return v*v*(3-2*v)
def rr(d,b,fill,outline=INK,w=3,r=10): d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=w)
def line(d,p,fill=INK,w=4): d.line(p,fill=fill,width=w,joint="curve")
def poly(d,p,fill,outline=INK,w=3):
    d.polygon(p,fill=fill)
    if outline: d.line(p+[p[0]],fill=outline,width=w,joint="curve")
def ellipse(d,b,fill,outline=INK,w=3): d.ellipse(b,fill=fill,outline=outline,width=w)
def center(d,x,y,s,font,fill):
    b=d.textbbox((0,0),s,font=font); d.text((x-(b[2]-b[0])/2,y),s,font=font,fill=fill)
def capsule(d,a,b,fill,width,outline=INK,ow=3):
    line(d,[a,b],outline,width+ow*2); line(d,[a,b],fill,width)
    r=width//2
    for x,y in (a,b): ellipse(d,(x-r-ow,y-r-ow,x+r+ow,y+r+ow),fill,outline,ow)
def lerp(a,b,t): return (int(a[0]+(b[0]-a[0])*t),int(a[1]+(b[1]-a[1])*t))

def background(kind,t):
    im=Image.new("RGB",(W,H),"#182536"); d=ImageDraw.Draw(im)
    if kind in ("bedroom","bedroom_close"):
        d.rectangle((0,0,W,480),fill="#24384c"); d.rectangle((0,480,W,H),fill="#55483f")
        rr(d,(70,55,390,355),"#172c43","#d7c4a4",7,8)
        d.rectangle((84,69,376,340),fill="#526e7b")
        d.rectangle((225,70,231,340),fill="#d2c2a7"); d.rectangle((84,205,376,211),fill="#d2c2a7")
        ellipse(d,(285,92,345,152),"#f1dca9",None,0)
        for k in range(34):
            x=(k*47-int(t*35))%278+88; y=(k*31+int(t*78))%255+78
            line(d,[(x,y),(x-8,y+17)],"#b8d0d0",2)
        poly(d,[(40,40),(88,40),(88,365),(40,385)],"#35485b",None,0)
        poly(d,[(378,40),(420,40),(420,385),(378,365)],"#35485b",None,0)
        rr(d,(485,72,700,235),"#d9c8ad",INK,5,3); rr(d,(500,87,685,220),"#78929a",None,0,0)
        poly(d,[(500,220),(560,142),(615,200),(680,132),(680,220)],"#425d66",None,0)
        d.rectangle((850,125,1170,137),fill="#9a6a4e")
        for i,c in enumerate(("#718b83","#b88b5d","#61788e")):
            rr(d,(880+i*68,70,920+i*68,125),c,INK,2,4)
        poly(d,[(490,410),(1190,410),(1240,455),(460,455)],"#a87550",INK,5)
        d.rectangle((500,455,535,690),fill="#503c34"); d.rectangle((1160,455,1195,690),fill="#503c34")
        rr(d,(790,260,1035,407),"#161f2b","#d9e4df",5,10); rr(d,(804,275,1021,385),"#7899a4",None,0,4)
        center(d,912,315,"FOCUS",F_SMALL,"#e8e0cb")
        poly(d,[(780,407),(1045,407),(1080,425),(752,425)],"#aab2b1",INK,3)
        rr(d,(585,390,725,425),"#e8dfcf",INK,3,4)
        for y in (400,411): line(d,[(600,y),(710,y)],"#9b9da0",2)
        rr(d,(1090,385,1135,430),"#e8dfcf",INK,3,7); ellipse(d,(1122,394,1150,424),"#e8dfcf",INK,3)
        line(d,[(1155,400),(1168,315),(1200,300)],"#d7c7a9",10)
        poly(d,[(1170,287),(1235,287),(1220,325),(1180,325)],"#f1d39b",INK,3)
        if kind=="bedroom_close":
            for k in range(3):
                a=1+0.12*math.sin(t*11+k)
                ellipse(d,(690-k*13,368-k*13,722+k*13,445+k*13),"#f3c96c",None,0)
    elif kind=="bus":
        d.rectangle((0,0,W,H),fill="#283746"); d.rectangle((0,540,W,H),fill="#1b2732")
        rr(d,(35,38,1245,425),"#172b3d","#e5d4b7",8,20)
        for j,x in enumerate((65,355,645,935)):
            rr(d,(x,66,x+245,380),"#6f929e",INK,5,8)
            d.rectangle((x+12,82,x+233,365),fill="#8ca9ac")
            for i in range(5):
                bx=x+((i*57-int(t*115))%245); bh=90+(i%3)*55
                d.rectangle((bx,365-bh,bx+38,365),fill=("#9b755d","#617984","#bd966e")[i%3])
                for wy in range(380-bh,355,30): d.rectangle((bx+8,wy,bx+17,wy+13),fill="#f0d7a6")
            line(d,[(x+120,70),(x+120,375)],"#d9c7a8",4)
        for x in (270,620,970):
            line(d,[(x,0),(x,485)],"#d5b77f",11)
            rr(d,(x-52,325,x+52,500),"#506a7b",INK,5,18)
        d.rectangle((0,565,W,720),fill="#40474b")
        for x in range(0,W,180): line(d,[(x,575),(x+80,575)],"#c9b58e",4)
        rr(d,(90,475,430,585),"#536d7c",INK,6,20); rr(d,(835,475,1190,585),"#536d7c",INK,6,20)
    elif kind=="park":
        d.rectangle((0,0,W,405),fill="#9bb9b8"); d.rectangle((0,405,W,H),fill="#536f5c")
        ellipse(d,(970,58,1100,188),"#f2d99f",None,0)
        for x,y,r,c in [(80,310,145,"#47715f"),(315,300,115,"#5e876b"),(1020,315,160,"#47745e"),(1240,295,120,"#638a6b")]:
            d.rectangle((x-15,y,x+15,640),fill="#765540")
            ellipse(d,(x-r,y-r,x+r,y+r),c,INK,4)
            ellipse(d,(x-r*.55,y-r*.75,x-r*.1,y-r*.25),"#7da17a",None,0)
        poly(d,[(0,620),(1280,505),(1280,720),(0,720)],"#84936f",None,0)
        poly(d,[(420,720),(615,460),(710,460),(930,720)],"#c7b18b",None,0)
        rr(d,(745,455,1090,495),"#916b4d",INK,5,5)
        for y in (465,480): line(d,[(755,y),(1080,y)],"#c09368",3)
        line(d,[(790,490),(770,610)],"#594431",12); line(d,[(1040,490),(1060,610)],"#594431",12)
        for k in range(5):
            x=(k*260+int(t*28))%W; y=350+(k%3)*38+int(6*math.sin(t*2+k))
            ellipse(d,(x,y,x+8,y+8),"#e9d7ae",None,0)
        line(d,[(180,260),(180,500)],"#263b3b",7); ellipse(d,(160,240,200,270),"#f4dda5",None,0)
    return im

def draw_character(d,cx,base,scale,pose,t,reach=0):
    s=scale
    def P(x,y): return (int(cx+x*s),int(base+y*s))
    ellipse(d,(int(cx-80*s),int(base-8*s),int(cx+95*s),int(base+14*s)),"#202b32",None,0)
    if pose=="sit":
        hip=P(0,-178); knee1=P(72,-105); ankle1=P(78,-8); knee2=P(115,-105); ankle2=P(158,-8)
        capsule(d,hip,knee1,"#26313d",int(39*s)); capsule(d,knee1,ankle1,"#222d38",int(34*s))
        capsule(d,P(8,-178),knee2,"#26313d",int(38*s)); capsule(d,knee2,ankle2,"#222d38",int(32*s))
        rr(d,(ankle1[0]-8,ankle1[1]-8,ankle1[0]+55*s,ankle1[1]+13*s),"#111a24",INK,3,9)
        rr(d,(ankle2[0]-8,ankle2[1]-8,ankle2[0]+58*s,ankle2[1]+13*s),"#111a24",INK,3,9)
    else:
        stride=math.sin(t*5)*10 if pose=="walk" else 0
        hip=P(-5,-178); k1=P(-22+stride,-95); a1=P(-28+stride,-7); k2=P(34-stride,-98); a2=P(48-stride,-7)
        capsule(d,hip,k1,"#26313d",int(40*s)); capsule(d,k1,a1,"#222d38",int(34*s))
        capsule(d,P(8,-178),k2,"#26313d",int(39*s)); capsule(d,k2,a2,"#222d38",int(34*s))
        for a in (a1,a2): rr(d,(a[0]-8*s,a[1]-7*s,a[0]+48*s,a[1]+13*s),"#111a24",INK,3,8)
    poly(d,[P(-54,-350),P(42,-350),P(74,-190),P(48,-165),P(-55,-165),P(-78,-195)],HOOD,INK,5)
    line(d,[P(-8,-337),P(-4,-255),P(9,-220)],"#72849a",3)
    rr(d,(int(cx-30*s),int(base-224*s),int(cx+34*s),int(base-190*s)),"#293d52",INK,2,7)
    line(d,[P(-18,-344),P(-9,-305)],"#c0c4bc",2); line(d,[P(4,-344),P(12,-302)],"#c0c4bc",2)
    line(d,[P(-58,-185),P(52,-185)],"#64778a",3)
    rr(d,(int(cx-17*s),int(base-390*s),int(cx+22*s),int(base-337*s)),SKIN,INK,3,5)
    ellipse(d,(int(cx-53*s),int(base-490*s),int(cx+48*s),int(base-370*s)),SKIN,INK,4)
    ellipse(d,(int(cx-57*s),int(base-445*s),int(cx-31*s),int(base-411*s)),"#a96850",INK,2)
    poly(d,[P(38,-442),P(60,-430),P(39,-420)],SKIN,INK,2)
    poly(d,[P(-55,-440),P(-61,-488),P(-35,-515),P(-18,-494),P(1,-525),P(18,-496),P(45,-510),P(55,-472),P(47,-443),P(15,-452),P(-8,-445)],"#171a20",INK,3)
    for x1,y1,x2,y2 in [(-42,-489,-32,-463),(-15,-501,-8,-470),(13,-499,18,-466),(36,-488,39,-463)]:
        line(d,[P(x1,y1),P(x2,y2)],"#3b3c43",2)
    ellipse(d,(int(cx+18*s),int(base-456*s),int(cx+26*s),int(base-448*s)),"#171923",None,0)
    line(d,[P(12,-465),P(30,-468)],"#171923",3)
    line(d,[P(38,-413),P(48,-410)],"#75473b",2)
    left_sh=P(-48,-330); left_el=P(-92,-270); left_wr=P(-80,-215)
    capsule(d,left_sh,left_el,HOOD,int(29*s)); capsule(d,left_el,left_wr,HOOD,int(25*s))
    ellipse(d,(left_wr[0]-10*s,left_wr[1]-12*s,left_wr[0]+13*s,left_wr[1]+13*s),SKIN,INK,2)
    r_sh=P(40,-330); default_el=P(92,-270); default_wr=P(145,-220)
    if pose=="sit": default_el=P(92,-280); default_wr=P(165,-258)
    if pose=="hold": default_el=P(90,-285); default_wr=P(143,-250)
    target=P(145,-220)
    if isinstance(reach,tuple): target=(int(reach[0]),int(reach[1]))
    elbow=lerp(default_el,target,.52)
    capsule(d,r_sh,elbow,HOOD,int(29*s)); capsule(d,elbow,target,HOOD,int(24*s))
    ellipse(d,(target[0]-8*s,target[1]-12*s,target[0]+20*s,target[1]+14*s),SKIN,INK,2)
    for j in range(3):
        line(d,[(target[0]+10*s,target[1]-7*s+j*6*s),(target[0]+20*s,target[1]-6*s+j*6*s)],"#8f5c49",2)

def phone(d,x,y,scale=1,glow=0):
    s=scale
    if glow>0:
        for k in range(3):
            r=(1+k*.28+glow*.12)*s
            ellipse(d,(x-25*r,y-48*r,x+25*r,y+48*r),None,"#f1c66a",3)
    rr(d,(int(x-22*s),int(y-42*s),int(x+22*s),int(y+42*s)),"#101923","#e2ece7",4,8)
    rr(d,(int(x-16*s),int(y-32*s),int(x+16*s),int(y+29*s)),"#6caec0",None,0,4)
    rr(d,(int(x-12*s),int(y-25*s),int(x+12*s),int(y-8*s)),"#d9e6df",None,0,3)
    ellipse(d,(int(x-3*s),int(y+33*s),int(x+3*s),int(y+38*s)),"#c7d4d0",None,0)

def draw_frame(t,idx,local):
    kind=SCENES[idx][2]; im=background(kind,t); d=ImageDraw.Draw(im)
    if idx==0:
        rr(d,(300,475,445,520),"#6c5548",INK,5,12); line(d,[(330,510),(320,650)],"#463b35",12); line(d,[(420,510),(438,650)],"#463b35",12)
        phone_x,phone_y=650,405; r=ease((local-.36)/.34)
        hand=lerp((614,361),(phone_x-2,phone_y+8),r)
        draw_character(d,430,650,1.12,"sit",t,hand)
        if local>.38: phone(d,phone_x,phone_y,1.0,clamp((local-.38)*2))
        if local<.4:
            for k in range(3): line(d,[(850+k*34,375),(865+k*34,375)],"#d8e9e6",2)
    elif idx==1:
        draw_character(d,480,770,1.42,"sit",t,(690,435))
        phone(d,760,410,1.85,.8+.2*math.sin(t*12))
        for k in range(8):
            a=k*math.pi/4; x=760+math.cos(a)*78; y=410+math.sin(a)*105
            line(d,[(x,y),(x+math.cos(a)*28,y+math.sin(a)*28)],"#f5d071",4)
        rr(d,(870,270,1170,350),"#f3e5c9",INK,4,12)
        center(d,1020,293,"NEW MESSAGE",F_SMALL,"#27394a")
        center(d,1020,318,"1 notification",F_TINY,"#4c6170")
    elif idx==2:
        rr(d,(330,440,650,565),"#526b7a",INK,5,20)
        draw_character(d,460,650,1.08,"hold",t,(620,390))
        phone(d,642,390,1.0,.2+.15*math.sin(t*8))
        for k in range(7):
            x=(k*190-int(t*90))%W; line(d,[(x,110),(x+55,110)],"#d5e2d8",2)
    else:
        phone_x,phone_y=800,430
        r=ease(local/.48)
        hand=lerp((540,410),(phone_x-4,phone_y+10),r) if local<.58 else lerp((phone_x-4,phone_y+10),(530,410),ease((local-.58)/.3))
        xshift=int(32*ease((local-.62)/.38))
        draw_character(d,600+xshift,650,1.08,"walk" if local>.68 else "stand",t,hand)
        phone(d,phone_x,phone_y,1.0,.1)
    d.rectangle((0,0,W,22),fill="#111923"); d.rectangle((0,H-18,W,H),fill="#111923")
    rr(d,(38,38,315,82),"#f2e5cf",INK,3,7)
    d.text((54,49),SCENES[idx][0],font=F_SMALL,fill="#25384b")
    rr(d,(48,620,1232,690),"#172638","#f1e3c9",3,10)
    cap=SCENES[idx][1]; x=75; y=641
    for j,w in enumerate(cap.split()):
        token=w+(" " if j<len(cap.split())-1 else "")
        d.text((x,y),token,font=F_CAP,fill="#f3cf71" if j==len(cap.split())-1 or j==2 else "#fff4e2")
        x+=d.textbbox((0,0),token,font=F_CAP)[2]
    for k in range(6):
        xx=1160+k*12; line(d,[(xx,98),(xx+8,112)],"#f1d59c",2)
    return im

def main():
    wav="renders/production-character-narration.wav"
    narration=" ".join(s[1] for s in SCENES)
    subprocess.run(["espeak-ng","-v","en-us","-s","145","-w",wav,narration],check=True)
    out="renders/wise-lab-production-character-20sec.mp4"
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,
         "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-af","apad","-t",str(DURATION),out]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for f in range(DURATION*FPS):
            t=f/FPS; idx=min(3,int(t/5)); local=(t-idx*5)/5
            frame=draw_frame(t,idx,local)
            zoom=1.0+.018*ease(local); cw,ch=int(W/zoom),int(H/zoom)
            frame=frame.crop((0,0,cw,ch)).resize((W,H),Image.Resampling.LANCZOS)
            if local<.12 and idx>0:
                frame=Image.blend(frame,Image.new("RGB",(W,H),"#101923"),.22*(1-local/.12))
            proc.stdin.write(frame.tobytes())
    except BrokenPipeError:
        pass
    finally:
        if proc.stdin and not proc.stdin.closed: proc.stdin.close()
    err=proc.stderr.read().decode("utf-8","replace"); code=proc.wait()
    if code: raise RuntimeError(f"FFmpeg failed ({code}): {err[-4000:]}")
    print(f"Rendered {DURATION*FPS} frames at {W}x{H}, {FPS}fps: {out}")
if __name__=="__main__": main()
