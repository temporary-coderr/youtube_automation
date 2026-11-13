from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess, wave

W,H,FPS=1280,720,24
OUT="renders/comic"
os.makedirs(OUT,exist_ok=True)
BG="#172235"; INK="#10131c"; PAPER="#f4e7cf"; SKIN="#b8795b"
try:
    title=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",38)
    capfont=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",27)
    small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",17)
    tiny=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",14)
except OSError:
    title=capfont=small=tiny=ImageFont.load_default()

def line(d,pts,fill=INK,width=5):
    d.line(pts,fill=fill,width=width,joint="curve")
def outlined(d,box,fill,outline=INK,width=5):
    d.rounded_rectangle(box,radius=8,fill=fill,outline=outline,width=width)
def text_center(d,xy,s,font,fill):
    b=d.textbbox((0,0),s,font=font); d.text((xy[0]-(b[2]-b[0])/2,xy[1]),s,font=font,fill=fill)

def draw_room(d,t,beat):
    # Layered room: wall, floor, skirting, rug, window, shelf, framed print, rain.
    d.rectangle((0,0,W,550),fill="#263a50")
    d.rectangle((0,550,W,H),fill="#182332")
    d.rectangle((0,535,W,550),fill="#8c6852")
    d.polygon([(0,590),(1280,560),(1280,720),(0,720)],fill="#202d3b")
    d.polygon([(120,630),(1080,600),(1180,690),(70,710)],fill="#354354")
    # window with moving rain and moon
    outlined(d,(62,58,360,330),"#101d33",PAPER,10)
    d.ellipse((265,86,315,136),fill="#f5dfa6")
    line(d,[(210,62),(210,325)],PAPER,7); line(d,[(68,194),(355,194)],PAPER,7)
    for k in range(22):
        x=(k*53+int(t*55))%290+70; y=(k*37+int(t*93))%250+70
        line(d,[(x,y),(x-7,y+17)],"#6d8ba0",2)
    # wall shelf and objects
    d.rectangle((850,105,1195,123),fill="#8c6047",outline=INK,width=4)
    for x,c in [(885,"#527d75"),(930,"#b98a5d"),(975,"#6e8494")]:
        d.rectangle((x,55,x+28,105),fill=c,outline=INK,width=3)
    d.ellipse((1090,63,1148,121),fill="#d5c49d",outline=INK,width=4)
    line(d,[(1119,91),(1119,72)],INK,3); line(d,[(1119,91),(1133,99)],INK,3)
    outlined(d,(450,85,650,220),"#e9d9bd",INK,5)
    d.rectangle((466,101,634,203),fill="#77909a")
    d.polygon([(466,203),(545,135),(634,203)],fill="#354f58")
    d.ellipse((565,117,590,142),fill="#f5dfa6")
    # desk and legs
    d.polygon([(250,465),(1190,465),(1230,510),(220,510)],fill="#a36c49",outline=INK)
    d.rectangle((285,505,325,682),fill="#5b4035",outline=INK,width=4)
    d.rectangle((1120,505,1160,675),fill="#5b4035",outline=INK,width=4)
    # desk lamp with animated light pool
    d.ellipse((930,430,1170,510),fill="#b18a5b")
    line(d,[(1080,455),(1100,355),(1150,335)],"#d6c6a5",13)
    d.polygon([(1120,320),(1205,320),(1180,365),(1140,365)],fill="#e2c88d",outline=INK)
    d.ellipse((1080,465,1100,485),fill="#e4d2ae",outline=INK,width=3)
    # notebook, pencil, mug, phone and small plant
    outlined(d,(680,420,855,458),"#e9e1d0",INK,3)
    line(d,[(700,429),(835,429)],"#8c9298",2); line(d,[(700,441),(820,441)],"#8c9298",2)
    line(d,[(725,415),(790,393)],"#d8b16d",5)
    outlined(d,(880,425,930,475),"#e8e0d0",INK,4)
    d.ellipse((920,438,950,466),fill="#e8e0d0",outline=INK,width=4)
    d.arc((890,438,930,475),270,90,fill=INK,width=4)
    d.rectangle((102,440,135,488),fill="#6d8a68",outline=INK,width=3)
    for x,y in [(105,423),(88,432),(128,425),(117,410)]:
        d.ellipse((x-14,y-18,x+14,y+18),fill="#719b75",outline=INK,width=2)
    # phone glow
    glow=int(90+80*(.5+.5*math.sin(t*8)))
    outlined(d,(550,425,615,474),"#111827","#a9c8d5",4)
    d.rounded_rectangle((557,432,608,466),radius=4,fill=(20,glow,min(255,glow+35)))
    d.ellipse((598,422,613,437),fill="#ff665e",outline=INK,width=2)
    # soft light pool changes with notification
    if beat>=1:
        d.ellipse((490,390,680,510),fill=(55,85,112,35))

def draw_character(d,t,beat):
    # seated body with articulated shoulders/elbows/wrists, legs and planted shoes
    sway=math.sin(t*2.4)*4
    headx=405+sway
    # chair back
    outlined(d,(285,360,420,635),"#435365",INK,7)
    d.rectangle((310,600,395,625),fill="#303d4c",outline=INK,width=4)
    # legs and sneakers
    d.polygon([(365,535),(430,535),(465,650),(420,660)],fill="#202a37",outline=INK)
    d.polygon([(420,640),(500,650),(515,678),(418,678)],fill="#151c26",outline=INK)
    line(d,[(445,662),(493,662)],"#9aa7ad",3)
    d.polygon([(310,535),(370,535),(350,650),(300,650)],fill="#202a37",outline=INK)
    d.polygon([(300,635),(360,635),(375,675),(285,675)],fill="#151c26",outline=INK)
    line(d,[(306,660),(358,660)],"#9aa7ad",3)
    # torso hoodie silhouette
    d.polygon([(330,260),(465,260),(505,490),(300,490)],fill="#354456",outline=INK)
    line(d,[(395,275),(405,370),(420,400)],"#586779",4)
    line(d,[(345,320),(380,340),(395,365)],"#263343",4)
    outlined(d,(375,455,430,468),"#252f3b",INK,2)
    # neck and detailed head
    d.rectangle((378,226,423,280),fill=SKIN,outline=INK,width=4)
    d.ellipse((345,112,458,252),fill=SKIN,outline=INK,width=5)
    # ears, nose, eyes, brows
    d.ellipse((334,172,356,210),fill=SKIN,outline=INK,width=3)
    d.ellipse((447,172,469,210),fill=SKIN,outline=INK,width=3)
    line(d,[(370,168),(390,164)],"#29242a",4); line(d,[(414,164),(435,168)],"#29242a",4)
    d.ellipse((377,177,386,186),fill="#1b1b20"); d.ellipse((420,177,429,186),fill="#1b1b20")
    line(d,[(402,182),(397,204),(405,207)],"#80513f",3)
    line(d,[(390,224),(412,225)],"#653c36",3)
    # hair silhouette and locks
    d.pieslice((337,91,470,230),180,355,fill="#17191f",outline=INK,width=4)
    for pts in [[(345,157),(350,105),(375,127),(390,88),(408,125)],
                [(385,126),(415,91),(426,130),(452,106),(458,165)]]:
        d.polygon(pts,fill="#17191f",outline=INK)
    # arms: left rests near keyboard, right reaches phone after notification
    left_sh=(330,300); left_el=(300,390+math.sin(t*2)*3); left_wr=(340,438)
    d.line([left_sh,left_el,left_wr],fill="#354456",width=35,joint="curve")
    d.ellipse((left_el[0]-17,left_el[1]-17,left_el[0]+17,left_el[1]+17),fill="#354456",outline=INK,width=4)
    d.ellipse((left_wr[0]-13,left_wr[1]-13,left_wr[0]+13,left_wr[1]+13),fill=SKIN,outline=INK,width=3)
    # right arm smoothly transitions from keyboard to phone
    reach=max(0,min(1,(beat-0.2)/1.4))
    reach=reach*reach*(3-2*reach)
    shoulder=(462,305); elbow=(500+reach*35,390+reach*22+math.sin(t*3)*3)
    wrist=(560+reach*15,438+math.sin(t*3)*2)
    d.line([shoulder,elbow,wrist],fill="#354456",width=37,joint="curve")
    d.ellipse((elbow[0]-19,elbow[1]-19,elbow[0]+19,elbow[1]+19),fill="#354456",outline=INK,width=4)
    d.ellipse((wrist[0]-15,wrist[1]-13,wrist[0]+15,wrist[1]+13),fill=SKIN,outline=INK,width=3)
    # fingers reaching and tapping the phone
    for i in range(3):
        fx=wrist[0]+12+i*5; fy=wrist[1]+(i-1)*6
        line(d,[(fx,fy),(fx+10,fy+5)],SKIN,5)

def draw_frame(t,beat,caption,word_index):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    draw_room(d,t,beat)
    draw_character(d,t,beat)
    # animated visual beats: notification pulse, phone shake, pencil roll, steam, motion accents
    phone_x=582+int(3*math.sin(t*11)) if beat>=1 else 582
    if beat>=1:
        d.ellipse((phone_x-28,397,phone_x+45,480),outline="#ffe17c",width=3)
        for k in range(3):
            yy=408+k*15
            line(d,[(phone_x+25,yy),(phone_x+39,yy-7)],"#ffe17c",3)
    # steam curls above mug
    for k in range(2):
        x=900+k*13; y=415-int((t*20+k*13)%25)
        d.arc((x,y,x+16,y+25),180,330,fill="#d6d5cf",width=2)
    # subtle moving speed lines when attention is pulled
    if beat>=1:
        for k in range(4):
            yy=260+k*20; x=650+int((t*100+k*65)%150)
            line(d,[(x,yy),(x+32,yy-7)],"#e8c66f",2)
    # comic frame border and beat tag
    d.rectangle((14,14,1266,706),outline=PAPER,width=7)
    tags=["01  THE QUIET MOMENT","02  A NEW DISTRACTION","03  THE REACH","04  LOST IN THE FEED"]
    outlined(d,(35,30,420,78),"#f4e7cf",INK,3)
    d.text((52,43),tags[beat],font=small,fill="#172235")
    # moving speech/narration box, current word highlighted
    outlined(d,(45,565,1235,684),"#111a29",PAPER,4)
    words=caption.split()
    x=80; y=608
    for i,w in enumerate(words):
        shown=w+" "
        color="#ffe27a" if i==word_index else "#fff4df"
        d.text((x,y),shown,font=capfont,fill=color)
        x+=d.textbbox((0,0),shown,font=capfont)[2]
        if x>1160:
            x=80; y+=34
    return im

def main():
    wav=OUT+"/narration.wav"
    with wave.open(wav,"rb") as wf: dur=wf.getnframes()/wf.getframerate()
    # Four story beats; timing is tied to the narration duration.
    captions=[
        "You sit down to focus and finally find your rhythm.",
        "Then your phone lights up with one tiny notification.",
        "Your hand reaches for it before you even decide.",
        "A moment later your attention has drifted away."
    ]
    total=math.ceil(dur*FPS)
    for f in range(total):
        t=f/FPS; beat=min(3,int(t/max(.001,dur/4)))
        local=(t/dur*4)-beat
        caption=captions[beat]
        wi=min(len(caption.split())-1,int(local*len(caption.split())))
        im=draw_frame(t,beat,caption,wi)
        # gentle camera drift and scale, varying by beat to avoid a frozen panel
        zoom=1.015+0.018*(.5+.5*math.sin(t*1.2))
        cw,ch=int(W/zoom),int(H/zoom)
        panx=int((W-cw)*(.25+.5*(beat%2)))
        pany=int((H-ch)*(.35+.2*math.sin(t*.6)))
        im=im.crop((panx,pany,panx+cw,pany+ch)).resize((W,H),Image.Resampling.LANCZOS)
        im.save(f"{OUT}/frame_{f+1:04d}.jpg",quality=92)
    subprocess.run([
        "ffmpeg","-hide_banner","-loglevel","error","-y",
        "-framerate",str(FPS),"-i",f"{OUT}/frame_%04d.jpg","-i",wav,
        "-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-shortest","renders/wise-lab-comic-20sec.mp4"
    ],check=True)
    print("Rendered",total,"animated comic frames; narration",round(dur,2),"seconds")

if __name__=="__main__":
    main()
