#!/usr/bin/env python3
"""WISE-LAB 2D cutout-character proof of concept.

A layered SVG puppet is drawn as designed vector artwork (not primitive stick limbs),
then animated with deterministic 2D transforms and rendered to MP4.
"""
import math, os, subprocess
from pathlib import Path
import cairosvg
from PIL import Image

W, H, FPS, DURATION = 1280, 720, 24, 7
FRAMES = FPS * DURATION
OUT = Path("renders/2d-character")
OUT.mkdir(parents=True, exist_ok=True)

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def smooth(a, b, t):
    return a + (b-a) * (clamp(t)**2 * (3-2*clamp(t)))

def lerp(a, b, t):
    return a + (b-a)*t

def svg_frame(t):
    # Action beats: notice -> reach -> grasp -> lift -> look at phone.
    reach = smooth(1.35, 3.15, t)
    grip = smooth(3.0, 3.65, t)
    lift = smooth(3.7, 5.25, t)
    settle = smooth(5.25, 6.0, t)
    phone_x = lerp(760, 628, lift)
    phone_y = lerp(478, 366, lift)
    # Elbow and wrist are articulated in screen-space. The hand tracks the prop.
    shoulder = (478, 351)
    wrist = (phone_x-18, phone_y+8)
    elbow = (lerp(532, 550, reach), lerp(410, 390, reach))
    # Slight elbow correction as the phone is lifted.
    elbow = (elbow[0]-18*lift, elbow[1]-16*lift)
    def p(v): return f"{v[0]:.1f},{v[1]:.1f}"
    arm = f"M {p(shoulder)} Q 510,365 {p(elbow)} Q 585,430 {p(wrist)}"
    arm_inner = f"M {p(shoulder)} Q 510,365 {p(elbow)} Q 585,430 {p(wrist)}"
    phone_rotation = lerp(0, -8, lift)
    head_turn = 2.5*math.sin(t*1.2) - 3*settle
    blink = 1 if int(t*FPS) % 91 not in (0,1,2) else .12
    phone_shadow_x = phone_x
    # Phone remains on desk until grasp begins, then follows the hand anchor.
    display_phone_x = lerp(760, phone_x, grip)
    display_phone_y = lerp(478, phone_y, grip)
    # Scene framing slowly pushes in, keeping character and prop readable.
    zoom = 1.0 + .018*smooth(0, 7, t)
    view_w, view_h = W/zoom, H/zoom
    view_x = (W-view_w)*.38
    view_y = (H-view_h)*.36
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{view_x:.2f} {view_y:.2f} {view_w:.2f} {view_h:.2f}">
<defs>
 <linearGradient id="wall" x2="0" y2="1"><stop stop-color="#26364b"/><stop offset="1" stop-color="#182637"/></linearGradient>
 <linearGradient id="floor" x2="0" y2="1"><stop stop-color="#75533f"/><stop offset="1" stop-color="#342a2b"/></linearGradient>
 <linearGradient id="hood" x2=".8" y2="1"><stop stop-color="#52677d"/><stop offset=".48" stop-color="#344b63"/><stop offset="1" stop-color="#202f43"/></linearGradient>
 <linearGradient id="skin" x2=".8" y2="1"><stop stop-color="#d49a76"/><stop offset="1" stop-color="#986044"/></linearGradient>
 <linearGradient id="hair" x2="0" y2="1"><stop stop-color="#29272a"/><stop offset="1" stop-color="#090e16"/></linearGradient>
 <linearGradient id="phone" x2="1" y2="1"><stop stop-color="#465666"/><stop offset="1" stop-color="#111c2b"/></linearGradient>
 <radialGradient id="lamp"><stop stop-color="#f6d39b" stop-opacity=".35"/><stop offset="1" stop-color="#f6d39b" stop-opacity="0"/></radialGradient>
 <filter id="shadow" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<!-- Illustrated bedroom: separate depth planes and props -->
<rect width="1280" height="720" fill="url(#wall)"/>
<path d="M0 545H1280V720H0Z" fill="url(#floor)"/>
<path d="M0 535H1280" stroke="#a27a58" stroke-width="5" opacity=".45"/>
<rect x="88" y="64" width="325" height="330" rx="9" fill="#101b2b" stroke="#9a7758" stroke-width="15"/>
<rect x="105" y="81" width="291" height="296" fill="#526b7e"/>
<path d="M105 270Q190 190 255 257T396 235V377H105Z" fill="#30465c"/>
<circle cx="325" cy="142" r="37" fill="#eadcb8"/>
<path d="M105 220H396M250 81V377" stroke="#bda17f" stroke-width="9"/>
<path d="M122 102L170 102L145 350L122 350Z" fill="#d2c5aa" opacity=".18"/>
<rect x="470" y="82" width="235" height="145" rx="4" fill="#172331" stroke="#b38b67" stroke-width="8"/>
<rect x="482" y="94" width="211" height="121" fill="#617b89"/>
<path d="M482 194L535 146L570 177L630 123L693 186V215H482Z" fill="#40596a"/>
<rect x="875" y="95" width="290" height="18" rx="5" fill="#79583f"/>
<rect x="892" y="114" width="15" height="120" fill="#4b3a32"/>
<rect x="1135" y="114" width="15" height="120" fill="#4b3a32"/>
<rect x="895" y="135" width="55" height="78" rx="4" fill="#8c7562"/>
<rect x="970" y="124" width="65" height="89" rx="4" fill="#d0c1a8"/>
<rect x="1055" y="142" width="70" height="71" rx="4" fill="#647b83"/>
<ellipse cx="1090" cy="332" rx="250" ry="250" fill="url(#lamp)"/>
<path d="M1090 215V300" stroke="#d5b88c" stroke-width="9"/>
<path d="M1035 218H1145L1125 174H1055Z" fill="#e5c18d" stroke="#4b3c35" stroke-width="4"/>
<ellipse cx="1090" cy="300" rx="120" ry="140" fill="url(#lamp)"/>
<!-- Bed and desk -->
<path d="M60 510H395V585H60Z" fill="#34465a" stroke="#182434" stroke-width="6"/>
<path d="M75 488Q120 445 220 476L260 515H75Z" fill="#d0c1ad" stroke="#273344" stroke-width="5"/>
<path d="M40 580H410V695H40Z" fill="#4b3a35"/>
<path d="M40 580H410" stroke="#9b7658" stroke-width="8"/>
<path d="M470 485H1195L1230 514H445Z" fill="#a87551" stroke="#382b2b" stroke-width="7"/>
<path d="M485 510V690M1175 510V690" stroke="#49352e" stroke-width="24"/>
<!-- Laptop, notebook, cup -->
<path d="M925 405L1088 405L1105 480H908Z" fill="#1b2939" stroke="#111923" stroke-width="6"/>
<path d="M937 414H1077L1088 465H927Z" fill="#5c8794"/>
<path d="M910 481H1110L1130 495H890Z" fill="#9da9a8" stroke="#27313d" stroke-width="4"/>
<path d="M555 455L665 455L690 478H540Z" fill="#ded4c0" stroke="#524a45" stroke-width="4"/>
<path d="M575 462H652M580 470H646" stroke="#9e9a8c" stroke-width="3"/>
<path d="M835 443H878V481H835Z" fill="#e4d6c1" stroke="#3d3a39" stroke-width="4"/>
<path d="M878 452Q902 450 892 472H878" fill="none" stroke="#e4d6c1" stroke-width="7"/>
<path d="M842 449H871" stroke="#79513e" stroke-width="5"/>
<!-- Character cast shadow -->
<ellipse cx="475" cy="650" rx="205" ry="27" fill="#101923" opacity=".45" filter="url(#shadow)"/>
<!-- Seated legs, side-facing; layered trouser seams and shoes -->
<path d="M420 480Q480 464 530 491L610 550Q642 576 619 601L580 609Q548 587 520 568L430 538Z" fill="#263342" stroke="#111b28" stroke-width="8" stroke-linejoin="round"/>
<path d="M520 554Q576 571 619 592L625 622Q617 639 586 641L511 624Q489 614 495 591Z" fill="#1d2938" stroke="#111b28" stroke-width="8"/>
<path d="M510 603Q555 614 610 616" fill="none" stroke="#647184" stroke-width="4" opacity=".7"/>
<path d="M575 627Q620 620 655 637Q670 647 661 660H548Q530 650 548 637Z" fill="#151c26" stroke="#090f17" stroke-width="7"/>
<path d="M560 647H655M578 636L590 648M603 633L615 647" stroke="#687887" stroke-width="3"/>
<path d="M393 477Q434 455 477 480L535 535Q550 554 529 575L490 584Q459 563 432 548L378 522Z" fill="#303d4e" stroke="#111b28" stroke-width="8"/>
<path d="M388 535Q433 553 490 573L500 607Q494 628 463 630L388 605Q366 590 373 567Z" fill="#202c3b" stroke="#111b28" stroke-width="8"/>
<path d="M380 600Q423 617 480 615" fill="none" stroke="#657284" stroke-width="4"/>
<path d="M432 617Q472 615 504 637Q520 649 507 662H395Q378 652 395 635Z" fill="#141c27" stroke="#080e16" stroke-width="7"/>
<path d="M402 649H500M425 628L438 645M450 625L463 644" stroke="#687887" stroke-width="3"/>
<!-- Torso: hoodie silhouette, panel seams, pocket, drawstrings -->
<path d="M382 340Q400 313 438 306L493 315Q530 330 548 374L571 489Q540 516 480 515Q414 514 368 488L377 390Z" fill="url(#hood)" stroke="#111b28" stroke-width="9" stroke-linejoin="round"/>
<path d="M405 343Q427 325 451 329L468 349L448 380L395 374Z" fill="#415b74" stroke="#182638" stroke-width="5"/>
<path d="M468 350Q502 355 518 385L540 475" fill="none" stroke="#718399" stroke-width="5" opacity=".75"/>
<path d="M385 462Q440 450 502 467L510 498Q449 514 380 489Z" fill="#293e55" stroke="#182638" stroke-width="5"/>
<path d="M417 471L415 489M484 473L486 493" stroke="#718398" stroke-width="3"/>
<path d="M459 344Q455 389 466 428" fill="none" stroke="#b4c0c4" stroke-width="4"/>
<path d="M482 344Q479 385 493 419" fill="none" stroke="#b4c0c4" stroke-width="4"/>
<path d="M458 424L466 435L474 424" fill="none" stroke="#b4c0c4" stroke-width="3"/>
<!-- Neck and detailed side-profile head -->
<path d="M422 305L425 342Q443 362 471 346L466 305Z" fill="url(#skin)" stroke="#6c4739" stroke-width="5"/>
<g transform="rotate({head_turn:.2f} 443 267)">
 <path d="M397 226Q399 173 450 168Q501 172 501 225L491 287Q481 321 449 326Q414 318 402 285Z" fill="url(#skin)" stroke="#593b33" stroke-width="7"/>
 <path d="M489 246Q510 250 510 263Q508 278 489 278" fill="#c98865" stroke="#754b3d" stroke-width="5"/>
 <path d="M487 270Q501 277 488 290L475 291" fill="none" stroke="#754b3d" stroke-width="4"/>
 <path d="M456 296Q470 305 485 295" fill="none" stroke="#754b3d" stroke-width="4" stroke-linecap="round"/>
 <ellipse cx="479" cy="248" rx="6" ry="{7*blink:.2f}" fill="#171923"/>
 <path d="M465 231Q480 224 492 232" fill="none" stroke="#382b29" stroke-width="6" stroke-linecap="round"/>
 <path d="M402 236Q387 205 407 181Q419 153 452 158Q484 150 500 184L496 216Q482 191 462 196Q445 204 432 190Q422 218 402 236Z" fill="url(#hair)" stroke="#080d14" stroke-width="6"/>
 <path d="M406 192Q388 168 414 158Q422 138 444 157Q456 137 471 158Q495 148 503 179L491 192Q473 178 461 187Q444 172 432 192Q420 181 406 202Z" fill="#171c25" stroke="#080d14" stroke-width="5"/>
 <path d="M409 185Q398 167 414 159M437 177Q430 155 447 151M465 178Q465 157 482 166" fill="none" stroke="#51515a" stroke-width="4" stroke-linecap="round"/>
 <path d="M407 242Q394 256 407 273" fill="none" stroke="#e0a17b" stroke-width="5"/>
</g>
<!-- Left arm relaxed on thigh -->
<path d="M390 357Q361 376 360 414L389 450Q405 461 421 444L413 420L430 386Z" fill="url(#hood)" stroke="#111b28" stroke-width="8" stroke-linejoin="round"/>
<path d="M376 414Q389 424 405 416" fill="none" stroke="#718399" stroke-width="4"/>
<path d="M390 443Q399 450 409 441L421 453Q416 471 397 469Q379 466 380 451Z" fill="url(#skin)" stroke="#704a3c" stroke-width="4"/>
<!-- Right arm is a true articulated layered cutout; sleeve, cuff and hand follow the prop -->
<path d="{arm}" fill="none" stroke="#111b28" stroke-width="43" stroke-linecap="round" stroke-linejoin="round"/>
<path d="{arm_inner}" fill="none" stroke="url(#hood)" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{p(shoulder)} Q 512,366 {p(elbow)}" fill="none" stroke="#72869b" stroke-width="3" opacity=".7"/>
<path d="M{p((wrist[0]-17,wrist[1]+1))}L{p(wrist)}" stroke="#1a2a3c" stroke-width="25" stroke-linecap="round"/>
<path d="M{p((wrist[0]-17,wrist[1]+1))}L{p(wrist)}" stroke="#60758b" stroke-width="17" stroke-linecap="round"/>
<!-- palm and curled fingers: close around phone during grip beat -->
<g transform="translate({wrist[0]:.1f} {wrist[1]:.1f}) rotate({-12*lift:.1f})">
 <path d="M-10 -13Q-2 -28 13 -21L27 -11Q35 -3 27 8L13 18Q-2 20 -13 8Z" fill="url(#skin)" stroke="#704a3c" stroke-width="4"/>
 <path d="M12 -15Q25 -21 29 -11Q32 -3 22 1" fill="none" stroke="#8c5946" stroke-width="4" stroke-linecap="round"/>
 <path d="M14 -5Q30 -10 32 0Q32 8 20 10" fill="none" stroke="#8c5946" stroke-width="4" stroke-linecap="round"/>
 <path d="M7 7Q21 10 23 18" fill="none" stroke="#8c5946" stroke-width="3"/>
</g>
<!-- Smartphone: on desk first, then follows the hand; screen and camera details -->
<g transform="translate({display_phone_x:.1f} {display_phone_y:.1f}) rotate({phone_rotation:.1f})">
 <ellipse cx="0" cy="52" rx="34" ry="9" fill="#111923" opacity="{.25*(1-lift):.2f}"/>
 <rect x="-24" y="-54" width="48" height="100" rx="10" fill="url(#phone)" stroke="#080f18" stroke-width="5"/>
 <rect x="-19" y="-48" width="38" height="86" rx="7" fill="#0d1a29" stroke="#75838c" stroke-width="2"/>
 <rect x="-15" y="-31" width="30" height="39" rx="5" fill="#3d687d"/>
 <rect x="-12" y="-25" width="24" height="4" rx="2" fill="#d7e8e6"/>
 <rect x="-12" y="-16" width="19" height="3" rx="1.5" fill="#9bbcc2"/>
 <rect x="-12" y="-8" width="23" height="3" rx="1.5" fill="#9bbcc2"/>
 <circle cx="0" cy="27" r="3" fill="#b8c7c9"/>
 <circle cx="0" cy="-42" r="3" fill="#b8c7c9"/>
 <rect x="-19" y="-35" width="38" height="47" rx="4" fill="#b5d2d2" opacity="{.2*grip:.2f}"/>
</g>
<!-- Contact sparkle only at the moment of pickup -->
<g opacity="{grip*(1-lift)*.9:.2f}" stroke="#f3d28d" stroke-width="4" stroke-linecap="round">
 <path d="M{phone_x+34:.1f} {phone_y-25:.1f}l12 -12M{phone_x+43:.1f} {phone_y-5:.1f}l16 -2M{phone_x-34:.1f} {phone_y-25:.1f}l-10 -11"/>
</g>
<!-- Cinematic caption and scene label -->
<rect x="42" y="36" width="275" height="44" rx="8" fill="#101b2b" opacity=".9"/>
<text x="62" y="65" font-family="DejaVu Sans" font-size="20" font-weight="bold" letter-spacing="2" fill="#e9d5b3">WISE-LAB • ATTENTION</text>
<rect x="42" y="630" width="1196" height="62" rx="12" fill="#111d2d" opacity=".94" stroke="#e2d2b8" stroke-width="2"/>
<text x="70" y="670" font-family="DejaVu Sans" font-size="28" font-weight="bold" fill="#fff3df">A single notification can pull you away from what matters.</text>
</svg>'''

def main():
    for i in range(FRAMES):
        t=i/FPS
        data=svg_frame(t).encode("utf-8")
        png=cairosvg.svg2png(bytestring=data, output_width=W, output_height=H)
        (OUT/f"frame_{i:04d}.png").write_bytes(png)
    mp4="renders/wise-lab-2d-cutout-phone-action.mp4"
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
         "-i",str(OUT/"frame_%04d.png"),"-c:v","libx264","-preset","veryfast",
         "-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",mp4]
    subprocess.run(cmd,check=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",mp4,
                    "-vf","fps=1,scale=640:-1,tile=4x2","-frames:v","1",
                    "renders/wise-lab-2d-cutout-contact.jpg"],check=True)
    report=subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration:stream=width,height,r_frame_rate,codec_name","-of","json",mp4],text=True)
    Path("renders/wise-lab-2d-cutout-report.json").write_text(report)
    print(f"Rendered {FRAMES} frames, {W}x{H}, {FPS}fps: {mp4}")

if __name__=="__main__":
    main()
