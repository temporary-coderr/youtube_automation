import React from "react";
import {AbsoluteFill, Audio, Sequence, interpolate, useCurrentFrame, staticFile, Easing} from "remotion";

const C = {ink:"#111827",cream:"#f4eee5",gold:"#e7b35d",blue:"#243b55",teal:"#3d7775",skin:"#bd8060",hood:"#263449"};
const Caption = ({children}) => <div style={{position:"absolute",bottom:76,left:180,right:180,textAlign:"center",fontFamily:"Arial,sans-serif",fontSize:43,fontWeight:700,color:"white",textShadow:"0 3px 18px #000, 0 1px 4px #000",letterSpacing:.2}}>{children}</div>;
const Grain = () => <div style={{position:"absolute",inset:0,opacity:.12,pointerEvents:"none",backgroundImage:"radial-gradient(#fff 0.55px, transparent 0.8px)",backgroundSize:"5px 5px",mixBlendMode:"soft-light"}}/>;
function Person({x=900,y=570,scale=1,turn=0}) {
 return <g transform={`translate(${x} ${y}) scale(${scale}) rotate(${turn})`}>
  <ellipse cx="0" cy="340" rx="150" ry="24" fill="#101827" opacity=".35"/>
  <path d="M-82 175 Q-130 260 -105 330 L-35 330 L-12 225 L15 330 L88 330 Q105 260 70 170Z" fill="#151f30"/>
  <path d="M-92 80 Q-150 115 -126 220 L-74 245 L-38 150 L40 150 L75 245 L128 218 Q143 125 82 78Z" fill={C.hood}/>
  <path d="M-38 85 Q-58 145 -42 195 L0 215 L42 195 Q57 145 38 85Z" fill="#1a2639"/>
  <path d="M-47 -25 Q-56 -110 8 -115 Q76 -105 59 -10 L45 55 Q20 88 -20 70 Q-52 45 -47 -25Z" fill={C.skin}/>
  <path d="M-57 -42 Q-82 -117 -23 -143 Q39 -172 70 -119 Q100 -89 58 -60 L34 -85 Q2 -54 -18 -72 L-42 -45Z" fill="#171a20"/>
  <path d="M-42 -8 Q-30 -15 -20 -8 M18 -8 Q30 -15 40 -8" stroke="#30201c" strokeWidth="5" fill="none" strokeLinecap="round"/>
  <path d="M-12 27 Q2 34 17 25" stroke="#6c3e35" strokeWidth="4" fill="none" strokeLinecap="round"/>
  <path d="M-86 100 Q0 68 87 100" stroke="#40516a" strokeWidth="12" fill="none"/>
 </g>
}
function WindowScene(){
 return <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute"}}>
  <defs><linearGradient id="night" x2="0" y2="1"><stop stopColor="#101b34"/><stop offset="1" stopColor="#38536b"/></linearGradient><linearGradient id="lamp" x2="0" y2="1"><stop stopColor="#f5c77c" stopOpacity=".8"/><stop offset="1" stopColor="#f5c77c" stopOpacity="0"/></linearGradient></defs>
  <rect width="1920" height="1080" fill="#172235"/><rect x="0" y="0" width="1920" height="720" fill="url(#night)"/>
  {Array.from({length:28},(_,i)=><circle key={i} cx={(i*173+51)%1920} cy={(i*83+29)%600} r={i%3+1} fill="#e6d8b7" opacity=".55"/>)}
  <rect x="1190" y="105" width="560" height="550" rx="12" fill="#0c1424" stroke="#65758b" strokeWidth="22"/>
  <rect x="1220" y="135" width="500" height="490" fill="#253c57"/>
  <path d="M1220 500 L1370 330 L1460 425 L1580 270 L1720 445 L1720 625 L1220 625Z" fill="#182c43"/>
  <path d="M1220 560 L1370 455 L1510 535 L1640 405 L1720 485 L1720 625 L1220 625Z" fill="#314e64"/>
  {Array.from({length:8},(_,i)=><rect key={i} x={1250+i*58} y={180+(i%3)*80} width="15" height="22" fill="#f6c77a" opacity=".55"/>)}
  <rect y="720" width="1920" height="360" fill="#403c3b"/>
  <path d="M0 750 Q600 690 1150 755 L1920 720 L1920 1080 L0 1080Z" fill="#66564b"/>
  <rect x="180" y="770" width="770" height="28" rx="10" fill="#8b6b50"/><path d="M250 798 L230 1040 M890 798 L910 1040" stroke="#322e31" strokeWidth="28"/>
  <rect x="500" y="690" width="310" height="18" rx="5" fill="#d0b18b"/><rect x="530" y="590" width="250" height="105" rx="8" fill="#172333" stroke="#b99c7d" strokeWidth="9"/><rect x="550" y="608" width="210" height="72" fill="#6b94a1"/>
  <Person x={1050} y={500} scale={1.15}/>
  <path d="M1000 850 Q1080 820 1150 850" stroke="#d8a96c" strokeWidth="8" fill="none" opacity=".5"/>
 </svg>
}
function HallScene(){
 return <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute"}}>
 <defs><linearGradient id="hall" x2="0" y2="1"><stop stopColor="#263d52"/><stop offset="1" stopColor="#b17e5a"/></linearGradient></defs>
 <rect width="1920" height="1080" fill="url(#hall)"/>
 <path d="M0 0 L640 0 L900 1080 L0 1080Z" fill="#344c5d"/><path d="M1920 0 L1280 0 L1020 1080 L1920 1080Z" fill="#263b4d"/>
 <path d="M640 0 L1280 0 L1920 1080 L0 1080Z" fill="#d1a77d" opacity=".12"/>
 {Array.from({length:7},(_,i)=><g key={i}><path d={`M${i*320-100} 0 L${i*320+120} 0 L${i*220+240} 1080 L${i*220-60} 1080Z`} fill="#e9c08f" opacity=".07"/><circle cx={160+i*270} cy={150+(i%2)*70} r="28" fill="#f4c77d" opacity=".85"/></g>)}
 <path d="M0 850 L1920 850 L1920 1080 L0 1080Z" fill="#2a3038"/>
 <path d="M800 1080 L960 500 L1120 1080" fill="#d7b18a" opacity=".18"/>
 <Person x={960} y={560} scale={1.5}/>
 </svg>
}
function PhoneScene(){
 return <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute"}}>
 <defs><linearGradient id="desk" x2="0" y2="1"><stop stopColor="#263d4b"/><stop offset="1" stopColor="#101c2b"/></linearGradient></defs>
 <rect width="1920" height="1080" fill="#111c2b"/><circle cx="1450" cy="250" r="420" fill="#31566a" opacity=".25"/>
 <path d="M0 680 Q650 600 1250 690 T1920 650 L1920 1080 L0 1080Z" fill="url(#desk)"/>
 <rect x="330" y="745" width="1250" height="35" rx="18" fill="#927458"/><path d="M420 780 L400 1080 M1500 780 L1530 1080" stroke="#5c493d" strokeWidth="38"/>
 <g transform="translate(1170 330) rotate(-12)"><rect x="-112" y="-200" width="224" height="400" rx="34" fill="#080d17" stroke="#b5c0c9" strokeWidth="9"/><rect x="-94" y="-174" width="188" height="340" rx="20" fill="#263c56"/><circle cx="0" cy="135" r="10" fill="#d7e1e5"/><rect x="-65" y="-135" width="130" height="28" rx="14" fill="#d9e6ed" opacity=".22"/><circle cx="0" cy="-42" r="44" fill="#f3c56f"/><path d="M-58 55 Q0 -5 58 55 L58 95 L-58 95Z" fill="#e9a66c"/></g>
 <Person x={700} y={500} scale={1.28}/>
 <path d="M1070 120 Q1300 0 1480 150" stroke="#f0c77f" strokeWidth="5" fill="none" opacity=".4" strokeDasharray="12 18"/>
 </svg>
}
function DawnScene(){
 return <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute"}}>
 <defs><linearGradient id="sky" x2="0" y2="1"><stop stopColor="#273e58"/><stop offset=".62" stopColor="#d58f6b"/><stop offset="1" stopColor="#edc28d"/></linearGradient></defs>
 <rect width="1920" height="1080" fill="url(#sky)"/><circle cx="1450" cy="330" r="145" fill="#f8d59a" opacity=".9"/>
 <path d="M0 700 L250 430 L440 680 L700 360 L980 720 L1210 480 L1450 720 L1680 400 L1920 690 L1920 1080 L0 1080Z" fill="#40576a"/>
 <path d="M0 810 L300 620 L540 820 L850 560 L1120 820 L1450 610 L1700 820 L1920 650 L1920 1080 L0 1080Z" fill="#263e4c"/>
 <path d="M0 900 Q500 820 1000 900 T1920 870 L1920 1080 L0 1080Z" fill="#182d36"/>
 <Person x={960} y={600} scale={1.32}/>
 <path d="M0 1010 Q600 940 1200 1000 T1920 970" stroke="#e6b983" strokeWidth="8" fill="none" opacity=".45"/>
 </svg>
}
const scenes = [
 {start:0, Component:WindowScene, title:"WHY YOUR BRAIN REPLAYS", sub:"THE MOMENTS YOU REGRET", caption:"Ever replay a tiny awkward moment for hours?"},
 {start:270, Component:HallScene, title:"YOUR BRAIN IS SCANNING", sub:"FOR SOCIAL THREATS", caption:"Your brain treats social mistakes like signals worth studying."},
 {start:540, Component:PhoneScene, title:"THE LOOP FEELS URGENT", sub:"BUT IT ISN'T DANGER", caption:"The memory feels important because your attention keeps returning to it."},
 {start:810, Component:DawnScene, title:"NOTICE IT. THEN RELEASE IT.", sub:"YOU ARE NOT THAT MOMENT.", caption:"Name the thought, learn what you can, and return to the present."}
];
function Scene({item}){
 const frame=useCurrentFrame(); const local=frame-item.start;
 const zoom=interpolate(local,[0,269],[1.04,1.14],{extrapolateRight:"clamp",easing:Easing.inOut(Easing.quad)});
 const pan=interpolate(local,[0,269],[-16,18],{extrapolateRight:"clamp"});
 const fade=interpolate(local,[0,16,250,269],[0,1,1,0],{extrapolateRight:"clamp"});
 return <AbsoluteFill style={{opacity:fade,background:C.ink}}>
  <AbsoluteFill style={{transform:`translateX(${pan}px) scale(${zoom})`}}><item.Component/></AbsoluteFill>
  <div style={{position:"absolute",top:95,left:130,right:130,opacity:interpolate(local,[0,35],[0,1],{extrapolateRight:"clamp"})}}>
   <div style={{fontFamily:"Arial",fontSize:24,fontWeight:700,letterSpacing:8,color:C.gold}}>WISE-LAB  /  HUMAN BEHAVIOUR</div>
   <div style={{fontFamily:"Arial",fontSize:72,fontWeight:900,letterSpacing:1,color:C.cream,marginTop:20,lineHeight:1.03}}>{item.title}</div>
   <div style={{fontFamily:"Arial",fontSize:33,fontWeight:700,letterSpacing:9,color:"#e8c18b",marginTop:16}}>{item.sub}</div>
  </div>
  <Caption>{item.caption}</Caption><Grain/>
 </AbsoluteFill>
}
export const WiseLabFilm = () => {
 const frame=useCurrentFrame();
 const opening=interpolate(frame,[0,35],[0,1],{extrapolateRight:"clamp"});
 return <AbsoluteFill style={{background:C.ink}}>
  {scenes.map((item,i)=><Sequence key={i} from={item.start} durationInFrames={270}><Scene item={item}/></Sequence>)}
  <Sequence from={0} durationInFrames={1080}><Audio src={staticFile("narration.mp3")} volume={0.92}/></Sequence>
  <div style={{position:"absolute",right:90,bottom:32,fontFamily:"Arial",fontSize:20,letterSpacing:5,color:"#f5eee0",opacity:.7}}>WISE-LAB</div>
 </AbsoluteFill>
};