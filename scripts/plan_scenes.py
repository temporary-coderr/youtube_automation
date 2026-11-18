#!/usr/bin/env python3
"""Create visual direction from the creator-supplied script without changing narration.

Gemini is optional and is restricted to visual direction. A deterministic planner is
used when no key is configured or the AI response fails validation.
"""
from __future__ import annotations
import json, os, re, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "narration.txt"
OUTPUT = ROOT / "src" / "generatedScenePlan.js"
CAST = ["alex", "maya", "ethan", "zoe", "oliver", "arthur"]
PLACES = ["cafe", "street", "bedroom", "bedroom-phone", "bedroom-dawn", "park", "office", "classroom", "library", "living-room"]
ACTIONS = ["idle", "gesture", "walk", "turn", "reach", "phone", "think", "sit"]
STICKERS = {"tag", "stat", "definition", "steps", "quote", "compare", "diagram", "timeline", "callout"}
PROPS = {"phone", "notebook", "mug", "backpack", "chair", "book", "lamp"}

def sentences_from_script(script: str) -> list[str]:
    # Sentence segmentation is for visual planning only; narration.txt remains untouched.
    parts = re.split(r"(?<=[.!?])\s+", script.strip())
    return [p.strip() for p in parts if p.strip()]

def groups_for(sentences: list[str], max_words: int = 24) -> list[list[int]]:
    groups, current, count = [], [], 0
    for i, sentence in enumerate(sentences):
        words = len(sentence.split())
        if current and count + words > max_words:
            groups.append(current); current=[]; count=0
        current.append(i); count += words
    if current: groups.append(current)
    return groups

def infer_place(text: str, index: int) -> str:
    t = text.lower()
    if any(w in t for w in ("phone", "notification", "message", "scroll", "screen", "text")): return "bedroom-phone"
    if any(w in t for w in ("school", "classroom", "teacher", "student", "lesson")): return "classroom"
    if any(w in t for w in ("office", "workplace", "meeting", "colleague", "laptop", "deadline")): return "office"
    if any(w in t for w in ("library", "book", "reading", "study", "research")): return "library"
    if any(w in t for w in ("living room", "family", "sofa", "parent", "house", "at home")): return "living-room"
    if any(w in t for w in ("sleep", "bed", "night", "alone", "bedroom", "midnight")): return "bedroom"
    if any(w in t for w in ("morning", "dawn", "wake", "tomorrow", "new day")): return "bedroom-dawn"
    if any(w in t for w in ("walk", "street", "commute", "outside", "leave")): return "street"
    if any(w in t for w in ("office", "workplace", "meeting", "colleague", "laptop", "deadline")): return "office"
    if any(w in t for w in ("school", "classroom", "teacher", "student", "lesson")): return "classroom"
    if any(w in t for w in ("library", "book", "reading", "study", "research")): return "library"
    if any(w in t for w in ("living room", "family", "sofa", "parent", "house", "at home")): return "living-room"
    if any(w in t for w in ("park", "calm", "present", "breathe", "nature", "move on")): return "park"
    if any(w in t for w in ("friend", "conversation", "people", "social", "awkward", "someone", "relationship")): return "cafe"
    return ["cafe", "street", "bedroom", "park"][index % 4]

PSYCHOLOGY_VISUALS = {
    "thought_loop": ("overthink","replay","ruminate","looping thoughts","stuck in your head"),
    "attention_trap": ("notification","distract","scroll","phone","interruption"),
    "social_mirror": ("compare","comparison","jealous","everyone else","social media"),
    "boundary_shield": ("boundary","say no","people pleasing","protect your time"),
    "focus_spotlight": ("focus","concentrate","deep work","single task"),
    "habit_cycle": ("habit","routine","trigger","cue","reward"),
    "memory_web": ("memory","remember","forget","recall","learning"),
    "stress_meter": ("stress","overwhelmed","anxiety","pressure","tense"),
    "confidence_ladder": ("confidence","self belief","small wins","progress","courage"),
    "emotional_wave": ("emotion","feeling","mood","sadness","anger","regulate"),
    "decision_fork": ("decision","choose","choice","options","trade off"),
    "sleep_rhythm": ("sleep","rest","bedtime","circadian","tired")
}

def infer_psychology_visual(text: str) -> str | None:
    t = text.lower()
    priority = ["thought_loop","attention_trap","social_mirror","boundary_shield","habit_cycle","stress_meter","confidence_ladder","decision_fork","sleep_rhythm","memory_web","emotional_wave","focus_spotlight"]
    for visual in priority:
        if any(term in t for term in PSYCHOLOGY_VISUALS[visual]):
            return visual
    return None

def infer_sticker(text: str, index: int):
    t = text.lower()
    visual = infer_psychology_visual(text)
    if any(w in t for w in ("step", "first", "second", "third", "try this", "practice")):
        result = {"type":"steps","label":"A PRACTICAL RESET","title":"Try this","items":["Notice the pattern","Name what is true","Choose your next action"],"tone":"mint"}
    elif any(w in t for w in ("versus", "instead", "but ", "rather than", "difference", "compare")):
        result = {"type":"compare","left":{"label":"THE REACTION","title":"Automatic response","text":"The first impulse."},"right":{"label":"THE CHOICE","title":"Intentional response","text":"A more considered next step."},"tone":"coral"}
    elif any(w in t for w in ("means", "called", "definition", "psychology", "pattern")):
        result = {"type":"definition","term":"The pattern","text":"A repeated response that shapes how we think and act.","tone":"blue"}
    elif visual:
        result = {"type":"tag","text":PSYCHOLOGY_VISUALS[visual][0].replace("_"," ").upper(),"tone":"gold"}
    else:
        return None
    if visual:
        result.update({"visual":visual,"motion":"dynamic","artSize":174})
    return result

def infer_props(text: str) -> list[str]:
    t=text.lower()
    props=[]
    if any(w in t for w in ("phone","notification","message","screen","scroll","text")): props.append("phone")
    if any(w in t for w in ("write","notes","journal","plan","list")): props.append("notebook")
    if any(w in t for w in ("coffee","tea","drink","cafe","cup")): props.append("mug")
    if any(w in t for w in ("book","read","reading","learn")): props.append("book")
    if any(w in t for w in ("bag","backpack","carry")): props.append("backpack")
    if any(w in t for w in ("sit","chair","desk","work")): props.append("chair")
    return props[:2]

def make_fallback_plan(script: str) -> dict:
    sentences = sentences_from_script(script)
    if not sentences: raise ValueError("scripts/narration.txt is empty")
    groups = groups_for(sentences)
    shots = []
    for n, indexes in enumerate(groups):
        excerpt = " ".join(sentences[i] for i in indexes)
        # Keep a stable two-person core, then introduce the wider fixed cast only when
        # the story itself signals a different age or relationship perspective.
        pair = ["alex", "maya"]
        low = excerpt.lower()
        if any(x in low for x in ("child", "kid", "school", "parent", "young")): pair = ["alex", "oliver"]
        elif any(x in low for x in ("older", "elder", "grandfather", "grandmother", "age", "retirement")): pair = ["alex", "arthur"]
        elif any(x in low for x in ("friend", "colleague", "challenge", "argue", "conversation")): pair = ["alex", "ethan" if n % 2 else "maya"]
        words = len(excerpt.split())
        duration = max(90, round(words * 60 * 30 / 140))
        action = "think" if any(x in low for x in ("think", "mind", "remember", "worry", "thought")) else "gesture"
        shots.append({
            "place": infer_place(excerpt, n), "title": f"SCENE {n+1:02d}",
            "caption": excerpt[:112], "durationInFrames": duration,
            "lead": {"x": 755 if n % 2 == 0 else 850, "y": 925, "action": action, "talk": False, "characterId": pair[0]},
            "friend": {"x": 1390, "y": 930, "action": "idle" if n % 2 == 0 else "turn", "talk": False, "characterId": pair[1]},
            "sticker": infer_sticker(excerpt, n), "props": infer_props(excerpt),
            "zoom": [1.0, 1.055 if n % 2 == 0 else 1.025], "pan": [0, -24 if n % 2 == 0 else 18],
            "camera": {"move":"push-in" if n % 2 == 0 else "tracking"},
        })
    return {"version":1,"source":"creator-script","visualDirector":"deterministic-fallback","shots":shots}

def request_gemini_plan(script: str, fallback: dict) -> dict | None:
    key = os.getenv("GEMINI_API_KEY")
    if not key: return None
    model = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
    excerpts = sentences_from_script(script)
    prompt = {
      "task":"Create visual direction for an already-written narration. Do not write, rewrite, summarize, add, remove, or reorder spoken words.",
      "script_sentences":excerpts,
      "allowed_character_ids":CAST,
      "allowed_environments":PLACES,
      "allowed_actions":ACTIONS,
      "allowed_sticker_types":sorted(STICKERS),\n      "allowed_psychology_visuals":sorted(PSYCHOLOGY_VISUALS),
      "allowed_props":sorted(PROPS),
      "rules":[
        "Use 2 to 7 distinct fixed characters across the entire video; at most 2 characters in any scene.",
        "A scene has one or two characters in lead/friend roles, chosen only from allowed IDs.",
        "Group adjacent sentence indexes into coherent visual beats. Every sentence index must appear exactly once, in original order.",
        "Use a suitable environment, meaningful action, and optional props from allowed_props. Use an explainer sticker only when it clarifies the script.",
        "Return JSON only: {beats:[{sentence_indexes:[0],place:'cafe',characters:['alex','maya'],lead_action:'gesture',friend_action:'idle',props:['mug'],sticker:null,camera:'push-in'}]}.",
        "Do not create new characters, new narration, dialogue, statistics, research claims or text not present in the script."
      ]
    }
    body = {"contents":[{"parts":[{"text":json.dumps(prompt)}]}],"generationConfig":{"responseMimeType":"application/json","temperature":0.35}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response: data=json.loads(response.read().decode())
        raw=data["candidates"][0]["content"]["parts"][0]["text"]
        parsed=json.loads(raw)
        beats=parsed.get("beats",[])
        covered=[i for beat in beats for i in beat.get("sentence_indexes",[])]
        if covered!=list(range(len(excerpts))) or len(covered)!=len(set(covered)): return None
        used={c for beat in beats for c in beat.get("characters",[])}
        if not 2 <= len(used) <= 7 or not used.issubset(set(CAST)): return None
        shots=[]
        for n,beat in enumerate(beats):
            indexes=beat["sentence_indexes"]
            if not indexes or indexes != list(range(indexes[0], indexes[-1]+1)): return None
            ids=beat.get("characters",[])
            if not isinstance(ids,list): return None
            if not 1 <= len(ids) <= 2 or any(x not in CAST for x in ids): return None
            place=beat.get("place")
            if place not in PLACES: return None
            excerpt=" ".join(excerpts[i] for i in indexes)
            sticker=beat.get("sticker")
            if sticker and not isinstance(sticker,dict): sticker=None
            if sticker and sticker.get("type") not in STICKERS: sticker=None
            required = {"tag":["text"],"stat":["value"],"definition":["term","text"],"steps":["items"],"quote":["text"],"compare":["left","right"],"diagram":["items"],"timeline":["items"],"callout":["title"]}
            if sticker and any(not sticker.get(field) for field in required.get(sticker["type"],[])): sticker=None
            if sticker and sticker.get("type")=="stat" and not any(str(n) in str(sticker.get("value","")) for n in re.findall(r"\d+(?:\.\d+)?%?",excerpt)):
                sticker=None
            if sticker is None: sticker=infer_sticker(excerpt,n)
            props=[p for p in beat.get("props",[]) if p in PROPS][:3] if isinstance(beat.get("props",[]),list) else []
            camera=beat.get("camera","push-in")
            camera_map={"push-in":([1.0,1.07],[0,-24]),"pull-back":([1.07,1.0],[0,0]),"tracking":([1.02,1.05],[-55,0]),"pan-left":([1.04,1.04],[55,0]),"pan-right":([1.04,1.04],[-55,0]),"over-shoulder":([1.08,1.12],[-35,-20]),"parallax":([1.0,1.05],[0,-18]),"locked":([1.0,1.0],[0,0])}
            zoom,pan=camera_map.get(camera,([1.0,1.05],[0,-20]))
            duration=max(90,round(len(excerpt.split())*60*30/140))
            shots.append({
              "place":place,"title":f"SCENE {n+1:02d}","caption":excerpt[:112],"durationInFrames":duration,
              "lead":{"x":755,"y":925,"action":beat.get("lead_action","gesture") if beat.get("lead_action") in ACTIONS else "gesture","talk":False,"characterId":ids[0]},
              "friend":{"x":1390,"y":930,"action":beat.get("friend_action","idle") if beat.get("friend_action") in ACTIONS else "idle","talk":False,"characterId":ids[1]} if len(ids)>1 else None,
              "sticker":sticker,"props":props,"zoom":zoom,"pan":pan,"camera":{"move":camera}
            })
        return {"version":1,"source":"creator-script","visualDirector":model,"shots":shots}
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError, TypeError, IndexError, AttributeError):
        return None

def main():
    script=SCRIPT.read_text(encoding="utf-8").strip()
    plan=request_gemini_plan(script, make_fallback_plan(script)) or make_fallback_plan(script)
    # If an AI plan has invalid legacy shot data, fail back to deterministic direction.
    if not plan.get("shots"): plan=make_fallback_plan(script)
    duration=sum(s["durationInFrames"] for s in plan["shots"])
    plan["durationInFrames"]=duration
    OUTPUT.write_text("export const GENERATED_SCENE_PLAN = "+json.dumps(plan,ensure_ascii=False,indent=2)+";\n",encoding="utf-8")
    print(f"Visual plan: {len(plan['shots'])} scenes, {len({s[k]['characterId'] for s in plan['shots'] for k in ('lead','friend') if s.get(k)})} fixed characters, {duration/30:.1f}s; source script unchanged.")

if __name__=="__main__": main()
