#!/usr/bin/env python3
import math, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
W,H,FPS,SECONDS=1280,720,24,12
OUT="renders/framebyframe-benchmark.mp4"; DIR="renders/fbf"
os.makedirs(DIR,exist_ok=True)
def ease(t):
 t=max(0,min(1,t)); return t*t*(3-2*t)
def rr(d,b,r,c,o=None,w=1): d.rounded_rectangle(tuple(map(int,b)),r,fill=c,outline=o,width=w)
def ln(d,p,c,w): d.line([(int(x),int(y)) for x,y in p],fill=c,width=w,joint="curve")
def el(d,b,c,o=None,w=1): d.ellipse(tuple(map(int,b)),fill=c,outline=o,width=w)
def frame(i):
 im=Image.new("RGB",(W,H)); pix=im.load()
 for y in range(H):
  c=(int(20+12*y/H),int(30+10*y/H),int(51+7*y/H))
  for x in range(W): pix[x,y]=c
 d=ImageDraw.Draw(im)
 rr(d,(25,25,505,390),14,(26,47,69),(84,101,119),7)
 for x,h in [(50,110),(112,165),(180,125),(245,190),(320,145),(390,172),(450,112)]:
  rr(d,(x,360-h,x+38,360),2,(18,31,49))
  for yy in range(360-h+15,350,27):
   for xx in range(x+8,x+35,14): rr(d,(xx,yy,xx+5,yy+8),1,(194,158,103))
 ln(d,[(265,25),(265,390)],(82,98,115),5); ln(d,[(25,205),(505,205)],(82,98,115),5)
 rr(d,(0,420,1280,720),0,(49,43,48)); ln(d,[(0,420),(1280,420)],(112,86,70),8)
 for y in range(480,720,70): ln(d,[(0,y),(1280,y)],(62,54,56),2)
 rr(d,(600,420,1200,458),8,(104,69,53),(155,113,83),3); rr(d,(650,455,680,690),6,(62,48,44)); rr(d,(1140,455,1170,690),6,(62,48,44))
 rr(d,(770,390,950,417),5,(221,208,179),(245,230,202),2)
 t=i/FPS; walk=ease((t-1)/3); reach=ease((t-4.2)/2.1); lift=ease((t-7)/1.5)
 x=300+120*walk; stride=math.sin(t*2*math.pi*1.15)*18*(1-reach)
 el(d,(x-85,650,x+85,680),(23,23,29))
 ln(d,[(x,535),(x-25+stride,600),(x-32+stride,650)],(24,27,34),40)
 ln(d,[(x,535),(x+30-stride,600),(x+36-stride,650)],(24,27,34),40)
 rr(d,(x-63+stride,641,x-8+stride,666),10,(15,17,23)); rr(d,(x+8-stride,641,x+65-stride,666),10,(15,17,23))
 el(d,(x-55,345,x+55,555),(48,54,67),(84,90,101),3)
 ln(d,[(x,375),(x,510)],(87,91,101),3); rr(d,(x-31,477,x+31,515),8,(39,44,55),(82,86,96),2)
 rr(d,(x-17,310,x+18,365),8,(151,104,79)); el(d,(x-48,220,x+48,330),(164,116,88),(72,50,43),3)
 el(d,(x-52,205,x+49,275),(28,27,30))
 for dx,yy in [(-37,222),(-18,207),(4,205),(26,214),(42,230)]: el(d,(x+dx-17,yy-17,x+dx+18,yy+16),(29,28,31))
 ln(d,[(x-40,370),(x-82,430),(x-75,492)],(48,54,66),26); el(d,(x-88,480,x-62,510),(164,116,88))
 ex= x+70+reach*(735-(x+70)); ey=430+reach*(370-430); hx=x+47+reach*(870-(x+47)); hy=385+reach*9
 ln(d,[(x+38,370),(ex,ey),(hx,hy)],(48,54,66),27); el(d,(hx-14,hy-13,hx+14,hy+14),(164,116,88))
 px=880-10*lift; py=380+10*lift
 rr(d,(px-20,py-38,px+20,py+38),7,(13,16,23),(145,156,168),3); rr(d,(px-15,py-29,px+15,py+27),4,(76,137,174)); rr(d,(px-8,py+31,px+8,py+34),2,(174,185,193))
 glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow); el(gd,(px-35,py-55,px+35,py+55),(88,180,226,32))
 im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(18))).convert("RGB")
 d=ImageDraw.Draw(im); rr(d,(52,54,420,112),14,(12,19,30)); d.text((78,72),"WISE-LAB  /  ATTENTION",fill=(215,222,231))
 return im
for i in range(SECONDS*FPS):
 frame(i).save(f"{DIR}/{i:04d}.png",compress_level=1)
 if (i+1)%48==0: print(f"FRAMES {i+1}/{SECONDS*FPS}",flush=True)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{DIR}/%04d.png","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",OUT],check=True)
print("DONE",OUT)
