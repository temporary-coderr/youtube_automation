#!/usr/bin/env python3
"""Fail-fast quality gate for WISE-LAB rendered preview MP4s."""
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageStat

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--report", default="renders/wise-lab-quality-report.json")
    ns=ap.parse_args()
    video=Path(ns.video)
    if not video.is_file() or video.stat().st_size < 100_000:
        raise SystemExit("QUALITY FAIL: MP4 missing or unexpectedly small")
    meta=json.loads(run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height,r_frame_rate","-of","json",str(video)]))
    streams=meta.get("streams",[])
    v=next((x for x in streams if x.get("codec_type")=="video"),None)
    if not v: raise SystemExit("QUALITY FAIL: no video stream")
    duration=float(meta.get("format",{}).get("duration",0))
    if (v.get("width"),v.get("height")) != (1280,720):
        raise SystemExit(f"QUALITY FAIL: expected 1280x720, got {v.get('width')}x{v.get('height')}")
    if duration < 9.5:
        raise SystemExit(f"QUALITY FAIL: preview too short ({duration:.2f}s)")
    with tempfile.TemporaryDirectory() as td:
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(video),"-vf","fps=1,scale=160:90","-frames:v","10",f"{td}/sample_%02d.jpg"])
        samples=sorted(Path(td).glob("sample_*.jpg"))
        if len(samples)<8: raise SystemExit(f"QUALITY FAIL: only {len(samples)} decoded sample frames")
        hashes=[]; brightness=[]; deviations=[]
        for p in samples:
            im=Image.open(p).convert("L")
            stat=ImageStat.Stat(im)
            brightness.append(round(stat.mean[0],2)); deviations.append(round(stat.stddev[0],2))
            hashes.append(hashlib.sha1(im.tobytes()).hexdigest())
        unique=len(set(hashes))
    if unique < 5: raise SystemExit(f"QUALITY FAIL: too many repeated frames ({unique} unique samples)")
    if max(brightness)-min(brightness) < 1.0 and max(deviations) < 2.0:
        raise SystemExit("QUALITY FAIL: frames appear nearly blank/static")
    report={"status":"passed","video":str(video),"bytes":video.stat().st_size,
            "duration_seconds":round(duration,3),"resolution":f"{v['width']}x{v['height']}",
            "sample_frames":len(samples),"unique_sample_frames":unique,
            "sample_brightness":brightness,"sample_contrast":deviations,
            "audio_stream_present":any(x.get("codec_type")=="audio" for x in streams),
            "note":"Technical preview checks only; visual storytelling and audio quality still require human review."}
    Path(ns.report).parent.mkdir(parents=True,exist_ok=True)
    Path(ns.report).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
