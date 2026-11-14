import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
FRAMES=ROOT/"renders/rigged-character-frames"
OUT=ROOT/"renders/wise-lab-rigged-character-12sec.mp4"
FRAMES.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    page=browser.new_page(viewport={"width":1920,"height":1080},device_scale_factor=1)
    page.goto((ROOT/"prototype/rigged_character_engine.html").as_uri(),wait_until="load")
    page.wait_for_function("typeof window.renderAt === 'function'")
    for i in range(288):
        page.evaluate("(t) => window.renderAt(t)",i/24)
        page.locator("#stage").screenshot(path=str(FRAMES/f"frame_{i:04d}.png"),animations="disabled")
        if (i+1)%48==0: print(f"RENDERED {i+1}/288",flush=True)
    browser.close()
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","24","-i",str(FRAMES/"frame_%04d.png"),"-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT)],check=True)
print(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height,nb_frames","-of","json",str(OUT)],text=True))
