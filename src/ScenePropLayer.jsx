import React from "react";

// Lightweight vector props that can be selected per scene. Coordinates are in the
// 1920x1080 scene space; the phone can be placed beside the lead for hand interaction.
export function ScenePropLayer({props=[],frame=0,lead,place}) {
  if (!props.length) return null;
  const bob=Math.sin(frame*.08)*3;
  return <g>
    {props.map((id,index)=>{
      const baseX=420+(index%4)*350, baseY=770+(index%2)*-95;
      const handAnchored=id==="phone" && lead && ["phone","reach","grasp"].includes(lead.action);
      const x=handAnchored ? lead.x+112 : baseX;
      const y=handAnchored ? lead.y-225+bob : baseY+bob;
      if(id==="phone" && place && place.startsWith("bedroom")) return null;
      return <g key={id+"-"+index} transform={"translate("+x+" "+y+") rotate("+Math.sin(frame*.035+index)*2+")"}>
        {id==="phone" && <g>
          <rect x="-34" y="-62" width="68" height="124" rx="12" fill="#111923" stroke="#b9c7cb" strokeWidth="4"/>
          <rect x="-27" y="-48" width="54" height="94" rx="5" fill="#6da9b2"/>
          <path d="M-19 -30 H18 M-19 -18 H10 M-19 -6 H20" stroke="#e7f0e8" strokeWidth="4" strokeLinecap="round"/>
          <circle cy="52" r="4" fill="#b9c7cb"/>
          <path d="M-27 -42 L27 -42" stroke="#e7c18e" strokeWidth="3"/>
        </g>}
        {id==="mug" && <g>
          <path d="M-35 -34 H29 L23 32 Q0 45 -28 32Z" fill="#b7d1ca" stroke="#425a60" strokeWidth="4"/>
          <path d="M28 -23 Q65 -30 55 3 Q50 20 25 12" fill="none" stroke="#b7d1ca" strokeWidth="10"/>
          <path d="M-12 -48 Q-27 -68 -10 -83 M10 -48 Q-4 -70 13 -88" stroke="#f0d9b7" strokeWidth="4" fill="none" opacity=".55"/>
        </g>}
        {id==="notebook" && <g>
          <path d="M-65 -45 Q-8 -58 0 -43 V45 Q-30 31 -65 45Z" fill="#e9dfc9" stroke="#75634f" strokeWidth="4"/>
          <path d="M0 -43 Q32 -58 65 -45 V45 Q32 31 0 45Z" fill="#fff4df" stroke="#75634f" strokeWidth="4"/>
          {[0,1,2].map(i=><path key={i} d={"M-49 "+(-20+i*19)+" H-9 M14 "+(-20+i*19)+" H49"} stroke="#a7a092" strokeWidth="3"/>)}
          <path d="M0 -43 V45" stroke="#b49b7a" strokeWidth="4"/>
        </g>}
        {id==="book" && <g>
          <path d="M-62 -48 Q-15 -62 0 -44 V50 Q-32 33 -62 47Z" fill="#d8c8a8" stroke="#705943" strokeWidth="4"/>
          <path d="M0 -44 Q27 -61 62 -48 V47 Q29 33 0 50Z" fill="#f3e7d0" stroke="#705943" strokeWidth="4"/>
          <path d="M-45 -18 H-10 M-45 -3 H-10 M15 -18 H46 M15 -3 H46" stroke="#9e8b70" strokeWidth="3"/>
        </g>}
        {id==="backpack" && <g>
          <path d="M-48 -40 Q-44 -75 0 -75 Q44 -75 48 -40 L54 50 Q0 75 -54 50Z" fill="#394b60" stroke="#182536" strokeWidth="5"/>
          <path d="M-28 -30 Q0 -52 28 -30 V20 H-28Z" fill="#526b80" stroke="#1e3041" strokeWidth="4"/>
          <path d="M-22 -64 Q-44 -26 -43 35 M22 -64 Q44 -26 43 35" stroke="#a6b3ba" strokeWidth="5" fill="none"/>
        </g>}
        {id==="lamp" && <g>
          <path d="M-8 48 L-4 -32 L4 -32 L8 48Z" fill="#c6a66f"/>
          <path d="M-48 -35 Q0 -82 48 -35 L34 -3 H-34Z" fill="#d6b47c" stroke="#705943" strokeWidth="4"/>
          <ellipse cy="50" rx="32" ry="8" fill="#705943"/>
          <ellipse cy="0" rx="52" ry="64" fill="#f5d69a" opacity={.12+.08*Math.sin(frame*.1)}/>
        </g>}
        {id==="chair" && <g>
          <rect x="-38" y="-80" width="76" height="78" rx="8" fill="#35495d" stroke="#1b2c3c" strokeWidth="5"/>
          <rect x="-48" y="-5" width="96" height="22" rx="7" fill="#465b70"/>
          <path d="M-35 15 L-45 85 M35 15 L45 85" stroke="#243548" strokeWidth="9"/>
        </g>}
      </g>;
    })}
  </g>;
}
