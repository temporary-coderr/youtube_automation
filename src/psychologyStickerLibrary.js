export const PSYCHOLOGY_STICKERS = Object.freeze({
  thought_loop:{label:"OVERTHINKING",tone:"coral",keywords:["overthink","replay","ruminate","looping thoughts"]},
  attention_trap:{label:"ATTENTION TRAP",tone:"gold",keywords:["notification","distract","scroll","phone","interruption"]},
  social_mirror:{label:"SOCIAL COMPARISON",tone:"blue",keywords:["compare","comparison","jealous","everyone else","social media"]},
  boundary_shield:{label:"PERSONAL BOUNDARIES",tone:"mint",keywords:["boundary","say no","people pleasing","protect your time"]},
  focus_spotlight:{label:"FOCUS",tone:"gold",keywords:["focus","concentrate","deep work","single task"]},
  habit_cycle:{label:"HABIT CYCLE",tone:"mint",keywords:["habit","routine","trigger","cue","reward"]},
  memory_web:{label:"MEMORY NETWORK",tone:"blue",keywords:["memory","remember","forget","recall","learning"]},
  stress_meter:{label:"STRESS RESPONSE",tone:"coral",keywords:["stress","overwhelmed","anxiety","pressure","tense"]},
  confidence_ladder:{label:"BUILD CONFIDENCE",tone:"gold",keywords:["confidence","self belief","small wins","progress","courage"]},
  emotional_wave:{label:"EMOTIONAL WAVE",tone:"coral",keywords:["emotion","feeling","mood","sadness","anger","regulate"]},
  decision_fork:{label:"THE CHOICE",tone:"blue",keywords:["decision","choose","choice","options","trade off"]},
  sleep_rhythm:{label:"SLEEP RHYTHM",tone:"blue",keywords:["sleep","rest","bedtime","circadian","tired"]}
});
export const PSYCHOLOGY_STICKER_IDS=Object.keys(PSYCHOLOGY_STICKERS);
export function getPsychologySticker(id){return PSYCHOLOGY_STICKERS[id]||null;}
