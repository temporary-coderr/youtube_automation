import React from "react";
import {useCurrentFrame} from "remotion";
import {GENERATED_CAPTIONS} from "./generatedCaptions";

// One narration-synchronized subtitle owner for the whole composition.
export function NarrationCaptionLayer() {
  const frame=useCurrentFrame();
  const active=GENERATED_CAPTIONS.find(c=>frame>=c.startFrame && frame<=c.endFrame);
  if(!active) return null;
  return <div style={{
    position:"absolute",left:"12%",right:"12%",bottom:58,zIndex:30,
    display:"flex",justifyContent:"center",pointerEvents:"none",
    fontFamily:"Arial,sans-serif",fontSize:34,fontWeight:800,lineHeight:1.22,
    letterSpacing:.1,textAlign:"center",color:"#fffaf0",
    textShadow:"0 3px 8px rgba(0,0,0,.95),0 0 18px rgba(0,0,0,.65)",
    padding:"10px 20px",background:"rgba(9,16,24,.38)",borderRadius:12
  }}>{active.text}</div>;
}
