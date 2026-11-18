import React from "react";
import {useCurrentFrame} from "remotion";
import {getPsychologySticker} from "./psychologyStickerLibrary";
const colors={gold:"#e6b66f",blue:"#86b9d1",coral:"#dc9279",mint:"#91b9a2"};
const base={fill:"none",strokeWidth:8,strokeLinecap:"round",strokeLinejoin:"round"};
export function PsychologyStickerArt({id,tone="gold",motion="dynamic",size=174}){
 const f=useCurrentFrame(),meta=getPsychologySticker(id); if(!meta)return null;
 const color=colors[tone||meta.tone]||colors.gold, live=motion!=="static";
 const drift=live?Math.sin(f*.075)*6:0, spin=live?f*.9:0, pulse=live?1+Math.sin(f*.12)*.04:1;
 const s={...base,stroke:color};
 let art=null;
 switch(id){
 case "thought_loop": art=<g><path d="M105 35 C35 12 15 90 54 120 C91 148 150 104 128 70 C111 45 77 57 78 84 Q80 103 108 91" {...s}/><path d="M95 79 l18 12 -18 10" {...s}/><g transform={"rotate("+spin+" 105 105)"}><path d="M105 8 l11 18 h-22Z" fill={color}/></g></g>;break;
 case "attention_trap": art=<g><rect x="68" y="45" width="74" height="128" rx="15" {...s}/><rect x="80" y="60" width="50" height="82" rx="5" fill={color} opacity=".16" stroke={color} strokeWidth="3"/><path d="M105 24 V43 M95 34 H115 M155 55 l18 -12 M158 92 h22 M153 130 l20 12" {...s}/>{[0,1,2].map(i=><circle key={i} cx={158+i*4} cy={55+i*37} r="7" fill={color}/>)}</g>;break;
 case "social_mirror": art=<g><path d="M105 22 Q160 30 158 100 Q155 166 105 181 Q55 166 52 100 Q50 30 105 22Z" {...s}/><path d="M105 48 V153 M105 66 Q80 62 77 86 M105 66 Q130 62 133 86" {...s}/><circle cx="105" cy="102" r="18" fill={color} opacity=".22"/></g>;break;
 case "boundary_shield": art=<g><path d="M105 20 L165 46 V100 Q160 153 105 184 Q50 153 45 100 V46Z" {...s}/><path d="M73 104 l22 22 43 -49" {...s} strokeWidth="11"/></g>;break;
 case "focus_spotlight": art=<g><path d="M105 18 L45 160 H165Z" fill={color} opacity=".17" stroke={color} strokeWidth="5"/><circle cx="105" cy="111" r="22" fill={color} opacity=".35"/><path d="M105 18 V3 M42 34 L28 20 M168 34 L182 20 M75 160 H135" {...s}/></g>;break;
 case "habit_cycle": art=<g><path d="M58 55 A64 64 0 0 1 160 70 l-21 -3 9 -18 M152 153 A64 64 0 0 1 50 137 l21 3 -9 18" {...s}/><circle cx="105" cy="105" r="25" fill={color} opacity=".22" stroke={color} strokeWidth="5"/></g>;break;
 case "memory_web": art=<g>{[[105,35,50,85],[105,35,160,85],[50,85,75,155],[160,85,135,155],[75,155,135,155]].map((a,i)=><path key={i} d={"M"+a[0]+" "+a[1]+" L"+a[2]+" "+a[3]} {...s} opacity=".7"/>)}{[[105,35],[50,85],[160,85],[75,155],[135,155]].map((p,i)=><circle key={i} cx={p[0]} cy={p[1]} r={i?10:15} fill={color}/>)}</g>;break;
 case "stress_meter": art=<g><path d="M40 145 A65 65 0 0 1 170 145" {...s} strokeWidth="12"/><path d={"M105 140 L"+(105+43*Math.cos(-2.2+Math.min(1,(f%100)/100)*1.5))+" "+(140+43*Math.sin(-2.2+Math.min(1,(f%100)/100)*1.5))} {...s}/><circle cx="105" cy="140" r="10" fill={color}/></g>;break;
 case "confidence_ladder": art=<g><path d="M45 170 V135 H78 V103 H111 V71 H144 V36 M125 36 L144 17 164 36" {...s} strokeWidth="10"/></g>;break;
 case "emotional_wave": art=<g><path d={"M8 "+(105+drift)+" C38 30 64 30 88 105 S138 180 164 105 S190 30 202 105"} {...s} strokeWidth="9"/></g>;break;
 case "decision_fork": art=<g><path d="M105 180 V112 Q105 91 84 76 L48 44 M105 112 Q105 91 126 76 L162 44 M32 45 L48 27 65 45 M145 45 L162 27 179 45" {...s} strokeWidth="10"/></g>;break;
 case "sleep_rhythm": art=<g><path d="M137 30 A73 73 0 1 0 171 145 A58 58 0 0 1 137 30Z" {...s} strokeWidth="9"/><circle cx="151" cy="58" r="4" fill={color}/><circle cx="172" cy="80" r="3" fill={color}/></g>;break;
 default: art=<circle cx="105" cy="105" r="62" {...s}/>;
 }
 return <svg width={size} height={size} viewBox="0 0 210 210" style={{overflow:"visible",transform:"scale("+pulse+")"}}><circle cx="105" cy="105" r="94" fill={color} opacity=".05"/><g transform={"translate(0 "+drift+")"}>{art}</g>{live&&<circle cx="105" cy="105" r="91" fill="none" stroke={color} strokeWidth="2" strokeDasharray="5 12" strokeDashoffset={-f*1.2} opacity=".35"/>}</svg>;
}
