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

