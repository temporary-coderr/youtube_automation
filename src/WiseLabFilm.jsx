import React from "react";
import {AbsoluteFill, Audio, Sequence, interpolate, useCurrentFrame, staticFile, Easing} from "remotion";

/*
 * WISE-LAB continuous-story proof:
 * 15 connected 4-second shots. Reusable cut-out character rig, animated limbs,
 * prop interactions, motivated camera reframes and match-cut transitions.
 * No paid APIs, external image services, stock footage or runtime model calls.
 */
const C={ink:"#101827",cream:"#f5eee2",gold:"#e7b35d",skin:"#bd8060",hood:"#29394d",dark:"#172334"};
const ease=Easing.inOut(Easing.cubic);
const clamp={extrapolateLeft:"clamp",extrapolateRight:"clamp"};
const mix=(f,points,values)=>interpolate(f,points,values,{...clamp,easing:ease});
const Caption=({children})=><div style={{position:"absolute",left:150,right:150,bottom:72,textAlign:"center",font:"700 39px Arial",letterSpacing:.2,color:"#fff",textShadow:"0 3px 16px #000,0 1px 4px #000"}}>{children}</div>;
const Grain=()=> <div style={{position:"absolute",inset:0,pointerEvents:"none",opacity:.075,backgroundImage:"radial-gradient(#fff .6px,transparent .9px)",backgroundSize:"5px 5px"}}/>;

function Character({x=960,y=670,s=1,pose="idle",f=0,shirt=C.hood,skin=C.skin}){
 const walk=Math.sin(f*.19), bob=pose==="walk"?Math.abs(walk)*10:Math.sin(f*.07)*2;
 const reach=pose==="reach"||pose==="phone"||pose==="wave";
 const arm=pose==="phone"?-62:pose==="reach"?-82:pose==="wave"?-112:pose==="think"?-35:pose==="walk"?walk*28:0;
 const other=pose==="walk"?-walk*28:pose==="think"?-48:pose==="phone"?18:0;
 const leg=pose==="walk"?walk*27:pose==="sit"?-14:0;
 const headTurn=pose==="turn"?mix(f,[0,35,90,119],[0,18,18,0]):pose==="phone"?12:0;
 return <g transform={`translate(${x} ${y+bob}) scale(${s})`}>
  <ellipse cx="0" cy="12" rx="115" ry="18" fill="#070d16" opacity=".34"/>
  <g transform="translate(-38 -8) rotate(${leg} 0 0)"><path d="M-26 -5 L-34 140 L-24 210 L12 210 L5 130 L18 4Z" fill="#151e2c"/><path d="M-30 194 L14 194 L25 214 L-42 214Z" fill="#0b111b"/></g>
  <g transform="translate(38 -8) rotate(${-leg} 0 0)"><path d="M-18 4 L-5 130 L-12 210 L27 210 L36 140 L26 -5Z" fill="#1b2636"/><path d="M-17 194 L29 194 L43 214 L-24 214Z" fill="#0b111b"/></g>
  <path d="M-65 -160 Q-115 -145 -112 -55 L-93 12 Q0 38 93 12 L112 -55 Q115 -145 65 -160Z" fill={shirt}/>
  <path d="M-54 -145 Q0 -112 54 -145" stroke="#53657a" strokeWidth="9" fill="none"/>
  <g transform={`translate(-82 -128) rotate(${arm} 0 0)`}><path d="M0 0 Q-34 32 -27 86 L-12 126" stroke={shirt} strokeWidth="35" fill="none" strokeLinecap="round"/><path d="M-12 119 Q-18 143 0 151" stroke={skin} strokeWidth="23" fill="none" strokeLinecap="round"/></g>
  <g transform={`translate(82 -128) rotate(${other} 0 0)`}><path d="M0 0 Q34 32 27 86 L12 126" stroke={shirt} strokeWidth="35" fill="none" strokeLinecap="round"/><path d="M12 119 Q18 143 0 151" stroke={skin} strokeWidth="23" fill="none" strokeLinecap="round"/></g>
  <g transform={`translate(0 -204) rotate(${headTurn})`}>
   <path d="M-53 -24 Q-65 -110 0 -118 Q68 -111 57 -20 L43 35 Q20 72 -18 57 Q-54 32 -53 -24Z" fill={skin}/>
   <path d="M-61 -47 Q-86 -120 -22 -148 Q34 -176 69 -128 Q95 -94 58 -62 L34 -91 Q4 -55 -19 -76 L-44 -46Z" fill="#171a20"/>
   <path d="M-37 -10 Q-26 -17 -16 -10 M16 -10 Q28 -17 38 -10" stroke="#30201c" strokeWidth="5" fill="none" strokeLinecap="round"/>
   <path d="M-10 26 Q2 32 15 25" stroke="#6c3e35" strokeWidth="4" fill="none" strokeLinecap="round"/>
  </g>
 </g>;
}
function Room({night=true,location="bedroom",f=0}){
 const outside=night?"#263d58":"#8bb3bd";
 return <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute"}}>
  <defs><linearGradient id="wall" x2="0" y2="1"><stop stopColor={night?"#18273b":"#d6c4a9"}/><stop offset="1" stopColor={night?"#35495a":"#a98e75"}/></linearGradient></defs>
  <rect width="1920" height="1080" fill="url(#wall)"/>
  {location==="bedroom"&&<><rect x="1190" y="100" width="470" height="470" rx="8" fill="#0c1524" stroke="#927d69" strokeWidth="24"/><rect x="1215" y="125" width="420" height="420" fill={outside}/><circle cx={mix(f,[0,119],[1450,1480])} cy="250" r="62" fill={night?"#f2d8a3":"#f4d28a"}/><path d="M1215 450 L1360 310 L1470 420 L1560 280 L1635 390 L1635 545 L1215 545Z" fill="#24394c"/><rect x="0" y="770" width="1920" height="310" fill="#55483f"/><rect x="180" y="750" width="930" height="34" rx="8" fill="#9a7858"/><path d="M250 784 L230 1080 M1040 784 L1070 1080" stroke="#302b2b" strokeWidth="30"/></>}
  {location==="cafe"&&<><rect y="790" width="1920" height="290" fill="#4c3b34"/><rect x="150" y="130" width="560" height="470" fill="#385568" stroke="#c39d74" strokeWidth="18"/><path d="M150 430 L710 430" stroke="#c39d74" strokeWidth="12"/><circle cx="330" cy="270" r="5" fill="#f7d79b"/><rect x="1120" y="670" width="620" height="24" fill="#9d7958"/><path d="M1180 694 L1160 930 M1680 694 L1700 930" stroke="#594536" strokeWidth="24"/><circle cx="1500" cy="480" r="95" fill="#27394b"/><path d="M1410 560 Q1500 500 1590 560 L1620 690 L1380 690Z" fill="#687b78"/></>}
  {location==="hall"&&<><path d="M0 0 L650 0 L920 1080 L0 1080Z" fill="#344c5d"/><path d="M1920 0 L1270 0 L1000 1080 L1920 1080Z" fill="#263b4d"/><path d="M0 850 L1920 850 L1920 1080 L0 1080Z" fill="#28313a"/>{Array.from({length:6},(_,i)=><g key={i}><rect x={i*340+70} y="150" width="160" height="430" fill="#d3a67a" opacity=".12"/><circle cx={i*340+150} cy="140" r="24" fill="#f3c87d"/></g>)}</>}
  {location==="park"&&<><circle cx="1480" cy="250" r="140" fill="#f5d29a"/><path d="M0 660 L240 430 L480 690 L720 380 L980 700 L1280 450 L1540 690 L1760 420 L1920 620 L1920 1080 L0 1080Z" fill="#506b65"/><path d="M0 820 Q500 720 1000 830 T1920 790 L1920 1080 L0 1080Z" fill="#263f3c"/><path d="M0 930 Q600 860 1200 930 T1920 900" stroke="#d8b58b" strokeWidth="10" fill="none" opacity=".5"/></>}
 </svg>;
}
function Phone({x=1160,y=690,scale=1,tilt=0,glow=0}){
 return <g transform={`translate(${x} ${y}) rotate(${tilt}) scale(${scale})`}><rect x="-62" y="-120" width="124" height="240" rx="19" fill="#080e18" stroke="#bac4cb" strokeWidth="7"/><rect x="-51" y="-104" width="102" height="207" rx="12" fill="#243e59"/><rect x="-34" y="-80" width="68" height="10" rx="5" fill="#d7e3e8" opacity=".35"/><circle cx="0" cy="-20" r="27" fill="#f0c66f" opacity={.65+glow*.35}/><path d="M-38 54 Q0 4 38 54 L38 74 L-38 74Z" fill="#e6a36e"/><circle cx="0" cy="90" r="5" fill="#dce4e8"/></g>;
}
function Shot({shot}){
 const f=useCurrentFrame(), t=f/119, fadeIn=interpolate(f,[0,12],[0,1],clamp), fadeOut=interpolate(f,[107,119],[1,0],clamp);
 const cam=shot.cam||0, zoom=1.04+0.045*Math.sin(t*Math.PI);
 const px=shot.px??900, py=shot.py??700;
 const pose=shot.pose||"idle";
 const charX=shot.walk?mix(f,[0,119],[shot.walk[0],shot.walk[1]]):px;
 const phoneX=shot.phoneX??1160;
 return <AbsoluteFill style={{background:C.ink,opacity:Math.min(fadeIn,fadeOut)}}>
  <AbsoluteFill style={{transform:`translateX(${cam+Math.sin(t*Math.PI*2)*8}px) scale(${zoom})`}}>
   <Room night={shot.night!==false} location={shot.place||"bedroom"} f={f}/>
   {shot.partner&&<Character x={1450} y={720} s={.9} shirt="#536b78" pose={shot.partnerPose||"idle"} f={f}/>}
   {shot.desk&&<><rect x="180" y="760" width="700" height="24" rx="8" fill="#9b795b"/><path d="M240 784 L225 1080 M820 784 L840 1080" stroke="#463a34" strokeWidth="25"/></>}
   {shot.phone&&<g transform={`translate(${mix(f,[0,35,80,119],[phoneX,phoneX+8,phoneX-8,phoneX])} 0)`}><Phone x={0} y={shot.phoneY||720} scale={shot.phoneScale||1} tilt={shot.phoneTilt||0} glow={Math.max(0,Math.sin(f*.3))}/></g>}
   {shot.person!==false&&<Character x={charX} y={py} s={shot.scale||1.18} pose={pose} f={f}/>}
   {shot.bubble&&<g opacity={interpolate(f,[10,24,92,110],[0,1,1,0],clamp)}><rect x="990" y="240" width="330" height="115" rx="28" fill="#f5eee2"/><path d="M1050 355 L1020 400 L1110 355" fill="#f5eee2"/><text x="1155" y="310" textAnchor="middle" fontSize="31" fontFamily="Arial" fill="#243447">{shot.bubble}</text></g>}
   {shot.motionLine&&<path d="M1080 520 Q1200 450 1320 520" stroke="#f0c77f" strokeWidth="7" strokeDasharray="10 15" fill="none" opacity={.7}/>}
  </AbsoluteFill>
  <div style={{position:"absolute",top:70,left:110,font:"700 22px Arial",letterSpacing:7,color:C.gold}}>WISE-LAB  /  HUMAN BEHAVIOUR</div>
  <Caption>{shot.caption}</Caption><Grain/>
 </AbsoluteFill>;
}
const shots=[
 {place:"cafe",night:false,px:720,py:710,scale:1.02,pose:"wave",partner:true,bubble:"So... anyway.",caption:"A tiny awkward moment happens."},
 {place:"cafe",night:false,px:720,py:710,scale:1.02,pose:"turn",partner:true,partnerPose:"turn",caption:"You notice a strange pause."},
 {place:"cafe",night:false,px:720,py:710,scale:1.02,pose:"think",partner:true,partnerPose:"walk",caption:"The other person moves on."},
 {place:"hall",night:false,px:mix(0,[0,119],[760,980]),py:730,scale:1.1,pose:"walk",walk:[760,980],caption:"But your mind keeps the moment."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"sit",desk:true,caption:"Hours later, it comes back."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"think",desk:true,bubble:"Why did I say that?",caption:"You replay what you should have said."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"reach",desk:true,phone:true,phoneX:1120,caption:"Then you reach for your phone."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"phone",desk:true,phone:true,phoneX:1010,phoneY:650,caption:"You check the conversation again."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"turn",desk:true,phone:true,phoneX:1010,phoneY:650,motionLine:true,caption:"Your attention feeds the loop."},
 {place:"hall",night:true,px:950,py:730,scale:1.22,pose:"walk",walk:[1100,900],caption:"Your brain is scanning for social threats."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"think",desk:true,caption:"But replaying is not protection."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"reach",desk:true,phone:true,phoneX:1030,phoneY:720,caption:"Name the thought. Don't argue with it."},
 {place:"bedroom",night:true,px:760,py:720,scale:1.18,pose:"idle",desk:true,phone:true,phoneX:1270,phoneY:790,phoneTilt:24,caption:"Keep the lesson. Let the rest pass."},
 {place:"park",night:false,px:960,py:730,scale:1.2,pose:"walk",walk:[760,1120],caption:"Bring your attention back to now."},
 {place:"park",night:false,px:1120,py:730,scale:1.2,pose:"idle",caption:"You are more than one awkward moment."}
];
export const WiseLabFilm=()=> <AbsoluteFill style={{background:C.ink}}>
 {shots.map((shot,i)=><Sequence key={i} from={i*120} durationInFrames={120}><Shot shot={shot}/></Sequence>)}
 <Sequence from={0} durationInFrames={1800}><Audio src={staticFile("narration.mp3")} volume={.94}/><Audio src={staticFile("ambience.wav")} volume={.2}/></Sequence>
 <div style={{position:"absolute",right:85,bottom:28,font:"700 19px Arial",letterSpacing:5,color:"#f5eee2",opacity:.8}}>WISE-LAB</div>
</AbsoluteFill>;
