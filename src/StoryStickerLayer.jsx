import React from "react";
import {interpolate,useCurrentFrame,Easing} from "remotion";
import {PsychologyStickerArt} from "./PsychologyStickerArt";
import {getPsychologySticker} from "./psychologyStickerLibrary";
const clamp={extrapolateLeft:"clamp",extrapolateRight:"clamp"};
const palettes={gold:{accent:"#e6b66f",glow:"rgba(230,182,111,.16)"},blue:{accent:"#86b9d1",glow:"rgba(134,185,209,.16)"},coral:{accent:"#dc9279",glow:"rgba(220,146,121,.16)"},mint:{accent:"#91b9a2",glow:"rgba(145,185,162,.16)"}};
export function StoryStickerLayer({spec}){
 const frame=useCurrentFrame(); if(!spec)return null;
 const meta=getPsychologySticker(spec.visual),p=palettes[spec.tone||meta?.tone||"gold"]||palettes.gold;
 const opacity=interpolate(frame,[0,8],[0,1],clamp),y=interpolate(frame,[0,14],[25,0],{...clamp,easing:Easing.out(Easing.back(1.12))});
 const base={position:"absolute",left:82,top:155,maxWidth:620,opacity,transform:"translateY("+y+"px)",fontFamily:"Arial,sans-serif",color:"#f8f0e3",pointerEvents:"none"};
 const panel={...base,padding:"18px 22px",borderRadius:18,background:"linear-gradient(135deg,rgba(13,23,33,.94),rgba(25,38,48,.88))",border:"1px solid rgba(238,222,197,.22)",boxShadow:"0 18px 55px rgba(0,0,0,.28)"};
 const eyebrow={fontSize:12,fontWeight:800,letterSpacing:2.5,color:p.accent,textTransform:"uppercase"},heading={fontSize:27,fontWeight:800,lineHeight:1.08,marginTop:8},body={fontSize:17,lineHeight:1.35,color:"#d6dce0",marginTop:8};
 const art=meta?<div style={{display:"flex",alignItems:"center",gap:14,marginBottom:spec.title||spec.note?8:0}}><PsychologyStickerArt id={spec.visual} tone={spec.tone||meta.tone} motion={spec.motion||"dynamic"} size={spec.artSize||174}/><div><div style={eyebrow}>{spec.label||meta.label}</div>{spec.title&&<div style={heading}>{spec.title}</div>}{spec.note&&<div style={body}>{spec.note}</div>}</div></div>:null;
 if(meta&&!spec.type)return <div style={{...base,display:"inline-block",padding:"10px 14px",borderRadius:18,background:"rgba(14,25,35,.86)",border:"1px solid rgba(238,222,197,.2)"}}>{art}</div>;
 if(spec.type==="tag")return <div style={{...base,display:"inline-block",padding:"10px 14px",borderRadius:18,background:"rgba(14,25,35,.86)",border:"1px solid rgba(238,222,197,.2)"}}>{art}<span style={{fontSize:16,fontWeight:800,letterSpacing:1.5}}>{spec.text}</span></div>;
 if(spec.type==="stat")return <div style={{...panel,borderLeft:"5px solid "+p.accent}}>{art}<div style={eyebrow}>{spec.label||"THE KEY IDEA"}</div><div style={{...heading,fontSize:46,color:p.accent}}>{spec.value}</div>{spec.note&&<div style={body}>{spec.note}</div>}</div>;
 if(spec.type==="definition")return <div style={panel}>{art}<div style={eyebrow}>PSYCHOLOGY, SIMPLIFIED</div><div style={heading}>{spec.term}</div><div style={body}>{spec.text}</div></div>;
 if(spec.type==="steps")return <div style={panel}>{art}<div style={eyebrow}>{spec.label||"TRY THIS"}</div><div style={heading}>{spec.title||"A simple reset"}</div><div style={{display:"grid",gap:9,marginTop:14}}>{(spec.items||[]).slice(0,3).map((item,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:11,fontSize:17}}><span style={{width:28,height:28,borderRadius:9,display:"grid",placeItems:"center",background:p.glow,border:"1px solid "+p.accent,color:p.accent,fontWeight:800}}>{i+1}</span>{item}</div>)}</div></div>;
 if(spec.type==="quote")return <div style={{...panel,borderLeft:"5px solid "+p.accent}}>{art}<div style={{fontSize:40,color:p.accent}}>“</div><div style={heading}>{spec.text}</div>{spec.source&&<div style={body}>{spec.source}</div>}</div>;
 if(spec.type==="compare")return <div style={{...panel,display:"grid",gridTemplateColumns:"1fr 1fr",gap:14}}>{art}{[spec.left,spec.right].map((item,i)=><div key={i}><div style={eyebrow}>{item.label}</div><div style={{...heading,fontSize:20}}>{item.title}</div><div style={body}>{item.text}</div></div>)}</div>;
 if(spec.type==="diagram"||spec.type==="timeline")return <div style={panel}>{art}<div style={eyebrow}>{spec.label||"HOW IT CONNECTS"}</div><div style={{display:"flex",gap:10,alignItems:"center",marginTop:18}}>{(spec.items||[]).slice(0,4).map((item,i)=><React.Fragment key={i}><div style={{flex:1,padding:"13px 9px",borderRadius:12,background:p.glow,border:"1px solid "+p.accent,textAlign:"center",fontWeight:800,fontSize:16}}>{item}</div>{i<(spec.items||[]).length-1&&<span style={{color:p.accent}}>→</span>}</React.Fragment>)}</div></div>;
 if(spec.type==="callout")return <div style={base}><div style={{...panel,borderLeft:"5px solid "+p.accent}}>{art}<div style={eyebrow}>{spec.label||"NOTICE THIS"}</div><div style={heading}>{spec.title||spec.text}</div>{spec.note&&<div style={body}>{spec.note}</div>}</div></div>;
 return meta?<div style={{...base,display:"inline-block",padding:"10px 14px",borderRadius:18,background:"rgba(14,25,35,.86)"}}>{art}</div>:null;
}
