import React from "react";
import {interpolate, useCurrentFrame, Easing} from "remotion";

const clamp = {extrapolateLeft:"clamp", extrapolateRight:"clamp"};
const enter = (f) => interpolate(f,[0,10],[0,1],{...clamp,easing:Easing.out(Easing.back(1.25))});
const palettes = {
  gold: {accent:"#e6b66f", glow:"rgba(230,182,111,.16)"},
  blue: {accent:"#86b9d1", glow:"rgba(134,185,209,.16)"},
  coral: {accent:"#dc9279", glow:"rgba(220,146,121,.16)"},
  mint: {accent:"#91b9a2", glow:"rgba(145,185,162,.16)"},
};

// Information overlays carry explanations; characters carry the story.
// Supported types: tag, stat, definition, steps, quote, compare.
export function StoryStickerLayer({spec}) {
  const frame = useCurrentFrame();
  if (!spec) return null;
  const p = palettes[spec.tone || "gold"] || palettes.gold;
  const opacity = interpolate(frame,[0,7],[0,1],clamp);
  const y = interpolate(frame,[0,12],[24,0],{...clamp,easing:Easing.out(Easing.cubic)});
  const base = {
    position:"absolute", left:88, top:170, maxWidth:520, opacity,
    transform:"translateY("+y+"px)", fontFamily:"Arial,sans-serif",
    color:"#f8f0e3", pointerEvents:"none",
  };
  const panel = {
    ...base, padding:"22px 26px", borderRadius:18,
    background:"linear-gradient(135deg,rgba(13,23,33,.94),rgba(25,38,48,.88))",
    border:"1px solid rgba(238,222,197,.22)",
    boxShadow:"0 18px 55px rgba(0,0,0,.28)",
  };
  const eyebrow = {fontSize:13, fontWeight:800, letterSpacing:3, color:p.accent, textTransform:"uppercase"};
  const heading = {fontSize:30, fontWeight:800, lineHeight:1.08, marginTop:9, letterSpacing:-.5};
  const body = {fontSize:18, lineHeight:1.4, color:"#d6dce0", marginTop:10};
  if (spec.type === "tag") return <div style={{...base,top:180,display:"inline-flex",alignItems:"center",gap:12,padding:"13px 19px",borderRadius:999,background:"rgba(14,25,35,.88)",border:"1px solid rgba(238,222,197,.24)"}}>
    <span style={{width:10,height:10,borderRadius:10,background:p.accent,boxShadow:"0 0 18px "+p.accent}}/>
    <span style={{fontSize:17,fontWeight:800,letterSpacing:2}}>{spec.text}</span>
  </div>;
  if (spec.type === "stat") return <div style={{...panel,top:190,borderLeft:"5px solid "+p.accent,background:"linear-gradient(120deg,"+p.glow+",rgba(13,23,33,.96) 55%)"}}>
    <div style={eyebrow}>{spec.label || "THE KEY IDEA"}</div>
    <div style={{...heading,fontSize:54,color:p.accent}}>{spec.value}</div>
    {spec.note && <div style={body}>{spec.note}</div>}
  </div>;
  if (spec.type === "definition") return <div style={panel}>
    <div style={eyebrow}>PSYCHOLOGY, SIMPLIFIED</div>
    <div style={heading}>{spec.term}</div>
    <div style={body}>{spec.text}</div>
  </div>;
  if (spec.type === "steps") return <div style={panel}>
    <div style={eyebrow}>{spec.label || "TRY THIS"}</div>
    <div style={heading}>{spec.title || "A simple reset"}</div>
    <div style={{display:"grid",gap:10,marginTop:16}}>
      {(spec.items || []).slice(0,3).map((item,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:12,fontSize:18,color:"#e9e4db"}}>
        <span style={{width:30,height:30,borderRadius:10,display:"grid",placeItems:"center",background:p.glow,border:"1px solid "+p.accent,color:p.accent,fontWeight:800}}>{i+1}</span>{item}
      </div>)}
    </div>
  </div>;
  if (spec.type === "quote") return <div style={{...panel,borderLeft:"5px solid "+p.accent}}>
    <div style={{fontSize:42,color:p.accent,lineHeight:.7}}>“</div>
    <div style={{...heading,fontSize:27}}>{spec.text}</div>
    {spec.source && <div style={{...body,fontSize:14,letterSpacing:1}}>{spec.source}</div>}
  </div>;
  if (spec.type === "compare") return <div style={{...panel,display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,maxWidth:650}}>
    {[spec.left,spec.right].map((item,i)=><div key={i}>
      <div style={{...eyebrow,color:i?p.accent:"#d99b82"}}>{item.label}</div>
      <div style={{fontSize:21,fontWeight:800,marginTop:9}}>{item.title}</div>
      <div style={{...body,fontSize:16}}>{item.text}</div>
    </div>)}
  </div>;
  if (spec.type === "callout") return <div style={{...base,top:210,display:"flex",alignItems:"center",gap:16,maxWidth:560}}>
    <div style={{width:7,height:72,borderRadius:8,background:p.accent,boxShadow:"0 0 22px "+p.accent}}/>
    <div style={{...panel,position:"relative",left:"auto",top:"auto",padding:"17px 22px"}}>
      <div style={eyebrow}>{spec.label || "NOTICE THIS"}</div>
      <div style={{...heading,fontSize:26}}>{spec.title || spec.text}</div>
      {spec.note && <div style={body}>{spec.note}</div>}
    </div>
  </div>;
  if (spec.type === "diagram") return <div style={{...panel,top:185,maxWidth:650}}>
    <div style={eyebrow}>{spec.label || "HOW IT CONNECTS"}</div>
    <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",gap:10,marginTop:22}}>
      {(spec.items || []).slice(0,3).map((item,i)=><React.Fragment key={i}>
        <div style={{flex:1,minHeight:74,padding:"14px 10px",borderRadius:12,background:p.glow,border:"1px solid "+p.accent,display:"grid",placeItems:"center",textAlign:"center",fontSize:17,fontWeight:800}}>{item}</div>
        {i < Math.min((spec.items || []).length,3)-1 && <span style={{color:p.accent,fontSize:24}}>→</span>}
      </React.Fragment>)}
    </div>
  </div>;
  if (spec.type === "timeline") return <div style={{...panel,top:205,maxWidth:650}}>
    <div style={eyebrow}>{spec.label || "THE SEQUENCE"}</div>
    <div style={{display:"flex",gap:12,marginTop:24}}>
      {(spec.items || []).slice(0,4).map((item,i)=><div key={i} style={{flex:1,position:"relative",paddingTop:18,borderTop:"3px solid "+p.accent}}>
        <span style={{position:"absolute",top:-9,left:0,width:14,height:14,borderRadius:20,background:p.accent,boxShadow:"0 0 14px "+p.accent}}/>
        <div style={{fontSize:16,fontWeight:800,lineHeight:1.2}}>{item}</div>
      </div>)}
    </div>
  </div>;
  return null;
}
