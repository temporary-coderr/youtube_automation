from PIL import Image, ImageDraw, ImageFont
import json, math, os, subprocess, wave

W,H,FPS=1280,720,24
OUT="renders/comic"
os.makedirs(OUT,exist_ok=True)
INK="#171923"; PAPER="#f5ead6"; SKIN="#b8795b"; HOOD="#34465a"
try:
    F_TITLE=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)
    F_CAP=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",25)
    F_SMALL=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",16)
except OSError:
    F_TITLE=F_CAP=F_SMALL=ImageFont.load_default()

PLAN_PATH="content/attention-trap-v3-scenes.json"
with open(PLAN_PATH, encoding="utf-8") as handle:
    SCENES=json.load(handle)

def validate_plan(scenes):
    allowed_poses={"standing_still","sitting","look_left","look_right","blink","breathe","hold_phone","put_away"}
    allowed_phone={"on_desk","in_hand_right","in_pocket","away","in_box","on_table"}
    allowed_micro={"rain_falling","lamp_glow_pulse","clock_tick","steam_from_mug","blink","monitor_flicker","buildings_scroll","phone_vibration","breathe","birds_flying","leaves_falling","signs_flicker","wind_lines","sun_glow_pulse"}
    if len(scenes)!=6:
        raise ValueError("v3 benchmark requires exactly six scenes")
    for i,s in enumerate(scenes,1):
        if s.get("scene_id")!=i or s.get("bg_locked") is not True:
            raise ValueError(f"Scene {i}: invalid id or bg_locked")
        if not 3 <= s.get("duration_sec",0) <= 12:
            raise ValueError(f"Scene {i}: duration must be 3-12 seconds")
        if s.get("camera",{}).get("transition_in")!="fade_to_black" or s.get("camera",{}).get("transition_out")!="fade_to_black":
            raise ValueError(f"Scene {i}: transitions must fade_to_black")
        ch=s.get("character",{})
        if ch.get("id")!="wise_man" or ch.get("pose") not in allowed_poses or not 0.97 <= ch.get("squash",1) <= 1.03:
            raise ValueError(f"Scene {i}: invalid locked character rig")
        if s.get("phone",{}).get("state") not in allowed_phone:
            raise ValueError(f"Scene {i}: invalid phone state")
        if len(s.get("micro_animations",[]))!=3 or any(x not in allowed_micro for x in s["micro_animations"]):
            raise ValueError(f"Scene {i}: exactly three approved micro animations required")
        words=s.get("caption","").split()
        if len(words)>12 or s.get("narration")!=s.get("caption") or s.get("keyword") not in s.get("caption",""):
            raise ValueError(f"Scene {i}: caption/narration/keyword validation failed")
    return True

validate_plan(SCENES)
BG_MAP={"bedroom_night":"bedroom","bus":"bus","office":"office","street":"street","park":"park"}
PAGES=[(s["title"],s["caption"],BG_MAP[s["bg"]]) for s in SCENES]
DURATION=sum(s["duration_sec"] for s in SCENES)

def poly(d,p,fill,outline=INK,w=4): d.polygon(p,fill=fill,outline=outline)
def rr(d,b,fill,outline=INK,w=4,r=10): d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=w)
def ln(d,p,fill=INK,w=4): d.line(p,fill=fill,width=w,joint="curve")
def txtc(d,x,y,s,font,fill):
    b=d.textbbox((0,0),s,font=font); d.text((x-(b[2]-b[0])/2,y),s,font=font,fill=fill)

def draw_background(d,scene,t):
    if scene in ("bedroom","desk"):
        d.rectangle((0,0,W,510),fill="#283b52"); d.rectangle((0,510,W,H),fill="#1a2736")
        # rain window, moon, curtains
        rr(d,(55,65,350,335),"#13253a",PAPER,8)
        d.ellipse((255,90,305,140),fill="#f6dfa8")
        ln(d,[(205,70),(205,330)],PAPER,6); ln(d,[(60,195),(345,195)],PAPER,6)
        for k in range(30):
            x=(k*43+int(t*50))%275+65; y=(k*31+int(t*80))%245+75
            ln(d,[(x,y),(x-6,y+15)],"#7693a5",2)
        # bed, pillow, blanket and bedside table
        rr(d,(830,365,1240,565),"#526477",INK,6,22)
        rr(d,(865,380,1045,445),"#e1d8c6",INK,4,18)
        poly(d,[(835,455),(1235,455),(1210,555),(850,555)],"#43566b")
        rr(d,(1040,450,1220,520),"#9b6c54",INK,4)
        # wall art and shelf
        rr(d,(480,80,690,220),"#e8d8bd",INK,5)
        d.rectangle((495,95,675,205),fill="#7b9299")
        poly(d,[(495,205),(560,135),(615,190),(675,135),(675,205)],"#415a61")
        d.rectangle((850,125,1180,140),fill="#98694e")
        for i,c in enumerate(["#698d80","#b68b5d","#6b8096"]):
            rr(d,(875+i*55,75,910+i*55,125),c,INK,2,4)
        # desk, laptop, notebook, lamp, mug, phone
        poly(d,[(170,430),(770,430),(820,475),(135,475)],"#a46e4a")
        d.rectangle((190,475,225,680),fill="#5b4035"); d.rectangle((730,475,765,680),fill="#5b4035")
        rr(d,(310,310,570,425),"#242c39",INK,6,12)
        d.rectangle((325,325,555,405),fill="#8ca5ae")
        d.rectangle((420,340,470,390),fill="#d9c7a2")
        rr(d,(585,415,720,450),"#eee5d5",INK,3,5)
        ln(d,[(600,425),(700,425)],"#9a9da1",2); ln(d,[(600,438),(690,438)],"#9a9da1",2)
        ln(d,[(620,410),(680,390)],"#d6b16d",5)
        rr(d,(745,405,790,455),"#e9e0d2",INK,3,7)
        d.ellipse((780,415,808,444),fill="#e9e0d2",outline=INK,width=3)
        ln(d,[(1070,420),(1090,325),(1140,310)],"#d8c6a1",12)
        poly(d,[(1110,295),(1195,295),(1175,340),(1130,340)],"#e7c98b")
        # phone screen and notification
        rr(d,(250,405,305,455),"#111923","#b7d2de",4,7)
        d.rectangle((257,412,298,445),fill="#6aacc3" if scene=="desk" else "#334b60")
        if scene=="desk":
            rr(d,(225,385,330,412),"#f6e6c5",INK,2,5)
            d.ellipse((307,378,324,395),fill="#ef625d")
    elif scene=="bus":
        d.rectangle((0,0,W,H),fill="#39495a"); d.rectangle((0,470,W,H),fill="#26313c")
        # bus interior with window, poles, seats
        rr(d,(45,55,1230,385),"#172a3d",PAPER,8,18)
        for x in (70,360,650,940):
            d.rectangle((x,70,x+250,365),fill="#7794a0",outline=INK,width=5)
            d.rectangle((x+20,90,x+230,340),fill="#526e7d")
        # passing city outside
        for i in range(9):
            x=(i*170-int(t*130))%1300
            d.rectangle((x,245-(i%3)*40,x+75,360),fill=["#bd956d","#6e8790","#a66d58"][i%3])
        for x in (180,560,930):
            ln(d,[(x,0),(x,440)],"#d3b47f",12)
            rr(d,(x-65,330,x+70,530),"#536b7b",INK,5,20)
        d.rectangle((0,555,W,580),fill="#c2a078")
    elif scene=="office":
        d.rectangle((0,0,W,520),fill="#d3d0c5"); d.rectangle((0,520,W,H),fill="#646e72")
        # office windows, partitions, plants, desk and monitors
        for x in (40,330,620):
            rr(d,(x,55,x+250,315),"#9cb3b6",INK,6,8)
            d.rectangle((x+15,70,x+235,300),fill="#7c9ba6")
            ln(d,[(x+125,65),(x+125,305)],PAPER,5)
        for x in (0,420,850):
            rr(d,(x,355,x+300,520),"#687e86",INK,5,12)
        poly(d,[(120,430),(1150,430),(1200,475),(75,475)],"#9b7658")
        for x in (250,800):
            rr(d,(x,300,x+190,420),"#202b38",INK,6,8)
            d.rectangle((x+12,312,x+178,395),fill="#7797a2")
        # files and coffee
        for i,c in enumerate(["#c16e58","#d7b16f","#6c8d80"]):
            rr(d,(1010+i*55,350,1050+i*55,425),c,INK,3,3)
        rr(d,(670,405,720,455),"#eee5d5",INK,3,6)
        d.ellipse((710,415,740,445),fill="#eee5d5",outline=INK,width=3)
        for k in range(3):
            x=700+k*12; y=395-int((t*20+k*8)%24)
            d.arc((x,y,x+18,y+24),180,340,fill="#fff0d8",width=2)
    elif scene=="street":
        d.rectangle((0,0,W,450),fill="#e1a875"); d.rectangle((0,450,W,H),fill="#48515b")
        # city buildings and signboards
        for i,(x,w,h,c) in enumerate([(0,230,390,"#596e7d"),(230,210,320,"#9b715b"),(440,250,430,"#526577"),(690,250,350,"#a77b60"),(940,340,410,"#566d79")]):
            d.rectangle((x,450-h,x+w,450),fill=c,outline=INK,width=4)
            for wx in range(x+20,x+w-15,55):
                for wy in range(450-h+25,425,65):
                    d.rectangle((wx,wy,wx+24,wy+32),fill="#e9d4a5")
        d.rectangle((0,510,W,560),fill="#333d48")
        for x in range(80,1280,220):
            d.rectangle((x,620,x+100,630),fill="#f3e4c6")
        rr(d,(850,90,1130,180),"#f1dfc3",INK,5)
        txtc(d,990,118,"ALWAYS ON",F_SMALL,"#263443")
        # street lamps
        for x in (120,1180):
            ln(d,[(x,250),(x,500)],"#242d37",8); ln(d,[(x,250),(x+45,250)],"#242d37",7)
            d.ellipse((x+30,240,x+58,262),fill="#ffe6a4")
    elif scene=="park":
        d.rectangle((0,0,W,420),fill="#a9c6c3"); d.rectangle((0,420,W,H),fill="#637d62")
        d.ellipse((930,55,1060,185),fill="#f6dda1")
        for x,y,r in [(120,330,130),(350,300,105),(1010,330,150),(1200,310,115)]:
            d.rectangle((x-14,y,x+14,610),fill="#765744")
            d.ellipse((x-r,y-r,x+r,y+r),fill="#527c68",outline=INK,width=4)
        poly(d,[(0,620),(1280,520),(1280,720),(0,720)],"#8a9b72")
        rr(d,(790,470,1110,530),"#8b674b",INK,5,10)
        ln(d,[(820,520),(800,640)],"#594331",12); ln(d,[(1080,520),(1100,640)],"#594331",12)
        # path and birds
        poly(d,[(420,720),(650,475),(750,475),(960,720)],"#c7b18a",None,0)
        for x,y in [(650,160),(710,195),(760,150)]:
            ln(d,[(x,y),(x+14,y-10),(x+28,y)],"#344b53",3)

def draw_person(d,t,scene,phase):
    # Character silhouette is drawn as a single connected pose, with joints and clothing seams.
    xbase={"bedroom":640,"desk":640,"bus":640,"office":640,"street":640,"park":640}[scene]
    bob=math.sin(t*5)*5
    x=xbase+int(math.sin(t*1.8)*12)
    # legs with changing stride
    stride=0  # v3 locked rig: no limb animation or foot sliding
    ln(d,[(x-25,470),(x-38+stride,570),(x-52+stride,635)],"#202b37",31)
    ln(d,[(x+25,470),(x+42-stride,565),(x+55-stride,635)],"#202b37",31)
    rr(d,(x-75+stride,625,x-15+stride,650),"#151d27",INK,3,8)
    rr(d,(x+30-stride,625,x+95-stride,650),"#151d27",INK,3,8)
    # torso and hoodie
    poly(d,[(x-65,285+bob),(x+60,285+bob),(x+90,475+bob),(x-90,475+bob)],HOOD)
    ln(d,[(x-12,300),(x-5,390),(x+12,420)],"#65758a",4)
    rr(d,(x-30,420,x+30,438),"#263342",INK,2,7)
    # neck and head
    d.rectangle((x-22,245+bob,x+22,300+bob),fill=SKIN,outline=INK,width=4)
    d.ellipse((x-62,130+bob,x+62,270+bob),fill=SKIN,outline=INK,width=5)
    d.ellipse((x-72,185+bob,x-48,220+bob),fill=SKIN,outline=INK,width=3)
    d.ellipse((x+48,185+bob,x+72,220+bob),fill=SKIN,outline=INK,width=3)
    d.pieslice((x-68,108+bob,x+68,255+bob),180,355,fill="#17191f",outline=INK,width=4)
    poly(d,[(x-62,165+bob),(x-48,110+bob),(x-22,132+bob),(x+2,98+bob),(x+25,132+bob),(x+56,115+bob),(x+65,175+bob)],"#17191f")
    d.ellipse((x-29,185+bob,x-18,196+bob),fill="#17191f")
    d.ellipse((x+18,185+bob,x+29,196+bob),fill="#17191f")
    ln(d,[(x-20,222+bob),(x+20,222+bob)],"#663e36",3)
    # arms with elbow bends; phone is reached for on page 2/3, relaxed on final page
    if scene in ("desk","bus","office"):
        arm1=[(x-58,315),(x-105,385),(x-50,420)]
        arm2=[(x+55,315),(x+110,380),(x+145,420)]
    elif scene=="park":
        arm1=[(x-58,315),(x-110,360),(x-135,405)]
        arm2=[(x+55,315),(x+105,360),(x+125,405)]
    else:
        arm1=[(x-58,315),(x-110,390),(x-90,445)]
        arm2=[(x+55,315),(x+110,380),(x+130,430)]
    for pts in (arm1,arm2):
        ln(d,pts,HOOD,31); d.ellipse((pts[1][0]-15,pts[1][1]-15,pts[1][0]+15,pts[1][1]+15),fill=HOOD,outline=INK,width=3)
        d.ellipse((pts[2][0]-12,pts[2][1]-12,pts[2][0]+12,pts[2][1]+12),fill=SKIN,outline=INK,width=3)
    # props: phone, tote/backpack, book depending on scene
    if scene in ("desk","bus","office"):
        px=x+145; py=405+int(4*math.sin(t*9))
        rr(d,(px-22,py-35,px+22,py+35),"#111923","#d2e7ed",3,7)
        d.rectangle((px-16,py-26,px+16,py+20),fill="#67abc4")
        d.ellipse((px+11,py-43,px+26,py-28),fill="#f05f5a")
    if scene=="park":
        rr(d,(x+95,400,x+155,450),"#b88b5d",INK,4,7)
        ln(d,[(x+108,405),(x+140,405)],"#e7d6b6",3)

def draw_page(t,scene_idx,local_t,caption,highlight):
    scene=PAGES[scene_idx][2]
    im=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(im)
    # paper texture and halftone dots
    d.rectangle((0,0,W,H),fill="#efe2ca")
    for yy in range(18,710,26):
        for xx in range(18,1270,26):
            if (xx//26+yy//26)%3==0: d.ellipse((xx,yy,xx+2,yy+2),fill="#d9c9ad")
    # inner comic frame and background scene
    rr(d,(25,25,1255,695),"#ffffff",INK,7,4)
    draw_background(d,scene,t)
    draw_person(d,t,scene,local_t)
    # foreground prop overlays unique to story page
    if scene=="bedroom":
        rr(d,(710,390,770,450),"#17202b","#d5e6e8",4,8)
        d.rectangle((718,400,762,438),fill="#263d50")
        txtc(d,740,408,"10:00",F_SMALL,"#e9e2d2")
    elif scene=="bus":
        rr(d,(1010,405,1180,480),"#f1e6d2",INK,4,9)
        txtc(d,1095,425,"NEXT STOP",F_SMALL,"#2d4052")
    elif scene=="office":
        rr(d,(90,420,190,480),"#a66f52",INK,4,7)
        d.rectangle((110,435,170,465),fill="#e8d7b8")
    elif scene=="street":
        rr(d,(80,390,255,470),"#e8d7b9",INK,4,8)
        txtc(d,167,415,"SALE",F_SMALL,"#34465a")
    # scene action marks, object movement
    if scene_idx in (1,2,3,4):
        pulse=1+0.2*math.sin(t*11)
        cx=760 if scene_idx==1 else 850
        d.ellipse((cx-34*pulse,390-34*pulse,cx+34*pulse,390+34*pulse),outline="#e7b94f",width=4)
        for k in range(3):
            ln(d,[(cx+38,365+k*16),(cx+58,357+k*16)],"#e7b94f",3)
    if scene=="park":
        for k in range(4):
            x=850+k*18; y=390-int((t*18+k*7)%25)
            d.arc((x,y,x+15,y+22),180,340,fill="#fff2d5",width=2)
    # page title label
    rr(d,(48,42,470,92),"#f6ead5",INK,3,6)
    d.text((66,54),PAGES[scene_idx][0],font=F_SMALL,fill="#263448")
    # narration mind-box, dynamic word highlight
    rr(d,(55,565,1225,670),"#182333",PAPER,4,10)
    words=caption.split(); x=82; y=602
    for i,w in enumerate(words):
        token=w+" "
        col="#ffe27b" if i==highlight else "#fff4df"
        d.text((x,y),token,font=F_CAP,fill=col)
        x+=d.textbbox((0,0),token,font=F_CAP)[2]
        if x>1165: x=82; y+=32
    return im

def page_turn(old,new,progress):
    # Comic page peel: incoming page slides from right while old page curls into a folded wedge.
    canvas=old.copy()
    cut=int(W*progress)
    if cut>0:
        canvas.paste(new.crop((W-cut,0,W,H)),(W-cut,0))
    fold_x=max(0,min(W, W-cut))
    if 0<fold_x<W:
        d=ImageDraw.Draw(canvas)
        d.polygon([(fold_x-28,0),(fold_x,0),(fold_x,H),(fold_x-28,H)],fill="#c6b99f")
        d.line([(fold_x-28,0),(fold_x-28,H)],fill=INK,width=3)
        d.polygon([(fold_x-28,0),(fold_x,18),(fold_x,H-18),(fold_x-28,H)],fill="#e8dcc5")
        d.line([(fold_x,18),(fold_x,H-18)],fill="#8f8779",width=2)
    return canvas

def main():
    wav=OUT+"/narration.wav"
    with wave.open(wav,"rb") as wf: duration=wf.getnframes()/wf.getframerate()
    page_dur=DURATION/len(PAGES)
    duration=DURATION\n    total=math.ceil(duration*FPS)
    prev=None
    for f in range(total):
        t=f/FPS
        idx=min(len(PAGES)-1,int(t/page_dur))
        local=(t-idx*page_dur)/page_dur
        cap=PAGES[idx][1]
        hi=min(len(cap.split())-1,int(local*len(cap.split())))
        page=draw_page(t,idx,local,cap,hi)
        # each page has gentle camera travel and a different crop focus
        zoom=1.015+0.022*(.5+.5*math.sin(local*math.pi))
        cw,ch=int(W/zoom),int(H/zoom)
        focus=[.25,.55,.72,.38,.65,.48][idx]
        px=int((W-cw)*focus); py=int((H-ch)*(.4+.15*math.sin(t*.7)))
        page=page.crop((px,py,px+cw,py+ch)).resize((W,H),Image.Resampling.LANCZOS)
        if idx>0 and local<0.24 and prev is not None:
            page=page_turn(prev,page,min(1,local/0.24))
        page.save(f"{OUT}/page_{f+1:04d}.jpg",quality=93)
        prev=draw_page(t,idx,local,cap,hi)
    os.makedirs("renders",exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
        "-i",f"{OUT}/page_%04d.jpg","-i",wav,"-c:v","libx264","-preset","veryfast",
        "-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",
        "renders/wise-lab-comic-20sec.mp4"],check=True)
    print(f"Rendered {len(PAGES)} illustrated pages, {total} frames, {duration:.2f}s narration")
if __name__=="__main__": main()
