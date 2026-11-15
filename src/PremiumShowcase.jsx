import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate, Easing} from "remotion";

const W=1920,H=1080;
const clamp={extrapolateLeft:"clamp",extrapolateRight:"clamp"};
const ease=Easing.inOut(Easing.cubic);
const mix=(f,a,b,x,y)=>interpolate(f,[a,b],[x,y],{...clamp,easing:ease});
const smooth=(v)=>v*v*(3-2*v);

function Rain({frame,count=90}){
  return <g opacity=".55">{Array.from({length:count},(_,i)=>{
    const x=(i*137+((frame*8+i*17)%2100))%2000-40;
    const y=(i*83+(frame*19+i*29)%1250)%1150-30;
    return <path key={i} d={`M${x} ${y} l-13 32`} stroke="#b8d7e7" strokeWidth={i%5===0?3:1.5} opacity={i%4===0?.8:.35}/>;
  })}</g>;
}

function Character({frame,x=920,y=875,scale=1,secondary=false}){
  const walk=frame<105?1-smooth(Math.max(0,frame-60)/45):0;
  const stride=Math.sin(frame*.19)*(walk);
  const bob=Math.abs(Math.sin(frame*.19))*10*walk + Math.sin(frame*.045)*2;
  const turn=mix(frame,72,120,0,-13);
  const blink=(frame%103>97 || frame%167>162);
  const armSwing=Math.sin(frame*.19)*26*walk;
  const reach=smooth(mix(frame,115,190,0,1));
  const shirt=secondary?"#bd8054":"#24394e";
  const pants=secondary?"#263044":"#172433";
  const skin=secondary?"#d09a79":"#b9785d";
  const hair=secondary?"#27201e":"#15171d";
  const s=scale;
  return <g transform={`translate(${x} ${y+bob}) scale(${s})`}>
    <ellipse cx="0" cy="0" rx="92" ry="15" fill="#050b12" opacity=".5"/>
    {/* legs and shoes */}
    <g transform={`rotate(${stride*28} -34 -155)`}>
      <path d="M-58 -190 Q-66 -105 -47 -26 L-42 -4 L7 -4 L12 -30 L-7 -190Z" fill={pants} stroke="#0d1722" strokeWidth="5"/>
      <path d="M-51 -92 L-10 -88 M-47 -39 L-9 -34" stroke="#657587" strokeWidth="3" opacity=".7"/>
      <path d="M-52 -15 Q-20 -25 12 -12 L23 6 Q12 19 -59 13 Q-76 7 -52 -15Z" fill="#111c28" stroke="#090f16" strokeWidth="4"/>
      <path d="M-65 4 Q-25 15 20 6" stroke="#a5b2b8" strokeWidth="3" fill="none"/>
    </g>
    <g transform={`rotate(${-stride*28} 35 -155)`}>
      <path d="M8 -190 Q-1 -110 25 -25 L31 -4 L80 -4 L80 -29 L62 -190Z" fill={pants} stroke="#0d1722" strokeWidth="5"/>
      <path d="M17 -92 L59 -88 M23 -39 L66 -34" stroke="#657587" strokeWidth="3" opacity=".7"/>
      <path d="M25 -15 Q55 -25 83 -12 L96 6 Q85 19 18 13 Q0 7 25 -15Z" fill="#111c28" stroke="#090f16" strokeWidth="4"/>
      <path d="M14 4 Q55 15 94 6" stroke="#a5b2b8" strokeWidth="3" fill="none"/>
    </g>
    {/* torso */}
    <path d="M-65 -420 Q-95 -365 -82 -245 L-70 -164 Q0 -137 76 -164 L84 -256 Q92 -365 57 -420 Q0 -450 -65 -420Z" fill={shirt} stroke="#101b28" strokeWidth="7"/>
    <path d="M-61 -400 Q-15 -376 0 -375 Q32 -378 61 -405" fill="none" stroke="#718194" strokeWidth="5" opacity=".7"/>
    <path d="M-8 -375 L-14 -183 M10 -375 L19 -183" stroke="#101d2a" strokeWidth="4" opacity=".65"/>
    <path d="M-63 -267 Q0 -250 69 -267" stroke="#506176" strokeWidth="3" opacity=".6" fill="none"/>
    {/* hoodie strings */}
    <path d="M-14 -365 Q-17 -325 -20 -290 M15 -365 Q18 -323 23 -291" stroke="#c3b8a5" strokeWidth="4" fill="none"/>
    <circle cx="-20" cy="-286" r="4" fill="#c3b8a5"/><circle cx="23" cy="-287" r="4" fill="#c3b8a5"/>
    {/* arms */}
    <g transform={`rotate(${-armSwing-8-reach*28} -61 -390)`}>
      <path d="M-61 -390 Q-112 -363 -128 -300 L-148 -226 Q-148 -204 -128 -200 Q-107 -197 -99 -220 L-77 -286 L-34 -350Z" fill={shirt} stroke="#101b28" strokeWidth="6"/>
      <path d="M-147 -222 Q-156 -198 -140 -184 Q-124 -174 -109 -193 L-99 -218 Q-119 -233 -147 -222Z" fill={skin} stroke="#744c42" strokeWidth="4"/>
      <path d="M-141 -191 l-7 17 M-129 -188 l-3 18" stroke="#e0aa8e" strokeWidth="3"/>
    </g>
    <g transform={`rotate(${armSwing+10+reach*15} 60 -390)`}>
      <path d="M60 -390 Q112 -364 126 -302 L143 -229 Q145 -205 125 -199 Q105 -197 96 -220 L76 -286 L34 -350Z" fill={shirt} stroke="#101b28" strokeWidth="6"/>
      <path d="M143 -228 Q158 -205 143 -187 Q128 -174 111 -194 L98 -220 Q120 -237 143 -228Z" fill={skin} stroke="#744c42" strokeWidth="4"/>
    </g>
    {/* neck and head */}
    <path d="M-24 -452 L-24 -410 Q0 -390 25 -410 L25 -452Z" fill={skin}/>
    <g transform={`rotate(${turn} 0 -520)`}>
      <path d="M-72 -580 Q-78 -670 0 -680 Q80 -668 73 -576 L61 -500 Q35 -444 0 -446 Q-45 -449 -65 -506Z" fill={skin} stroke="#754b40" strokeWidth="5"/>
      <path d="M-74 -601 Q-98 -660 -47 -696 Q8 -730 59 -690 Q94 -661 71 -600 L50 -625 Q12 -650 -18 -628 Q-44 -612 -74 -601Z" fill={hair} stroke="#0c1119" strokeWidth="6"/>
      <path d="M-66 -645 Q-38 -700 -4 -679 Q-30 -662 -33 -636 M-18 -665 Q20 -712 55 -665 Q27 -674 13 -641 M30 -661 Q68 -670 73 -626" fill={hair} stroke="#0c1119" strokeWidth="9" strokeLinecap="round"/>
      <path d="M-46 -566 Q-27 -578 -10 -568 M16 -568 Q35 -578 49 -565" stroke="#352a29" strokeWidth="6" fill="none" strokeLinecap="round"/>
      {blink?<path d="M-39 -545 q15 8 29 0 M20 -545 q14 8 27 0" stroke="#211c1b" strokeWidth="5" fill="none"/>:<><ellipse cx="-25" cy="-545" rx="5" ry="8" fill="#17191c"/><ellipse cx="33" cy="-545" rx="5" ry="8" fill="#17191c"/><circle cx="-27" cy="-548" r="2" fill="#fff"/><circle cx="31" cy="-548" r="2" fill="#fff"/></>}
      <path d="M1 -542 Q-5 -519 4 -515" stroke="#8c5d4f" strokeWidth="3" fill="none"/>
      <path d={frame%40<20?"M-12 -486 Q0 -480 13 -486":"M-12 -486 Q0 -477 13 -486"} stroke="#573a35" strokeWidth="4" fill="none" strokeLinecap="round"/>
      <path d="M-62 -514 Q-83 -510 -72 -482 Q-62 -467 -50 -483 M62 -514 Q83 -510 72 -482 Q62 -467 50 -483" fill={skin} stroke="#754b40" strokeWidth="4"/>
    </g>
    {/* jacket pocket and cuff detail */}
    <path d="M-48 -244 L-5 -237 L-12 -201 L-51 -207Z" fill="#1a2a3c" stroke="#718194" strokeWidth="3"/>
    <path d="M-67 -228 L-47 -222 M52 -228 L72 -222" stroke="#91a0ac" strokeWidth="4"/>
  </g>;
}

function ShowcaseScene(){
  const f=useCurrentFrame();
  const cameraX=mix(f,0,360,0,-115);
  const cameraZoom=mix(f,0,90,1,1.07)+mix(f,210,360,0,.035);
  const signGlow=.6+Math.sin(f*.08)*.12;
  const carX=mix(f,0,360,2180,-480);
  const puddle= .15+Math.sin(f*.11)*.035;
  const focus= f<115?0:f<220?1:2;
  return <AbsoluteFill style={{background:"#101b29"}}>
    <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
      <defs>
        <linearGradient id="sky" x2="0" y2="1"><stop stopColor="#101d31"/><stop offset=".58" stopColor="#263b50"/><stop offset="1" stopColor="#60717a"/></linearGradient>
        <linearGradient id="street" x2="0" y2="1"><stop stopColor="#35424b"/><stop offset="1" stopColor="#101820"/></linearGradient>
        <linearGradient id="window" x2="0" y2="1"><stop stopColor="#eabf79" stopOpacity=".9"/><stop offset="1" stopColor="#b86f4b" stopOpacity=".4"/></linearGradient>
        <radialGradient id="lamp"><stop stopColor="#ffdc9b" stopOpacity=".85"/><stop offset="1" stopColor="#ffbc70" stopOpacity="0"/></radialGradient>
        <filter id="blur"><feGaussianBlur stdDeviation="22"/></filter>
        <filter id="shadow"><feGaussianBlur stdDeviation="18"/></filter>
      </defs>
      <g transform={`translate(${cameraX} 0) scale(${cameraZoom})`}>
        <rect width="1920" height="1080" fill="url(#sky)"/>
        {/* distant skyline */}
        <g opacity=".8" fill="#17283a">
          <path d="M0 490V255H120V360H205V220H320V420H420V300H520V460H630V245H760V440H860V280H990V470H1110V225H1240V430H1350V300H1480V460H1600V235H1720V410H1830V285H1920V510Z"/>
          {Array.from({length:55},(_,i)=><rect key={i} x={(i*79)%1900} y={270+(i*43)%180} width="13" height="20" fill="#e5b97a" opacity=".45"/>)}
        </g>
        {/* cafe facade */}
        <path d="M1050 160 H1920 V760 H1050Z" fill="#1b2731"/>
        <path d="M1090 198 H1878 V680 H1090Z" fill="#2c3a43" stroke="#101820" strokeWidth="15"/>
        <g>
          <rect x="1120" y="225" width="345" height="425" fill="url(#window)" stroke="#111c26" strokeWidth="18"/>
          <rect x="1490" y="225" width="345" height="425" fill="url(#window)" stroke="#111c26" strokeWidth="18"/>
          <path d="M1290 225V650 M1660 225V650" stroke="#263744" strokeWidth="13"/>
          <path d="M1120 490H1465 M1490 490H1835" stroke="#263744" strokeWidth="9"/>
          <path d="M1145 255 L1435 610 M1510 255 L1805 610" stroke="#fff0d1" strokeWidth="5" opacity=".12"/>
        </g>
        <path d="M1040 190 H1880 L1920 135 H1090Z" fill="#c47c52"/>
        <path d="M1040 188 H1880" stroke="#f1c58a" strokeWidth="8"/>
        <rect x="1290" y="105" width="420" height="95" rx="12" fill="#18232d" stroke="#d7a66d" strokeWidth="6"/>
        <text x="1500" y="168" textAnchor="middle" fontSize="45" letterSpacing="10" fontWeight="800" fill="#f4d39c">NIGHT OWL</text>
        <circle cx="1500" cy="148" r="115" fill="url(#lamp)" opacity={signGlow} filter="url(#blur)"/>
        {/* warm interior silhouettes */}
        <g opacity=".8">
          <circle cx="1220" cy="420" r="37" fill="#493b35"/><path d="M1165 620 Q1170 490 1220 480 Q1275 495 1285 620Z" fill="#59463a"/>
          <path d="M1350 590 Q1380 515 1430 545 L1450 650H1330Z" fill="#574333"/>
          <circle cx="1700" cy="405" r="28" fill="#48372e"/><path d="M1660 630 Q1660 470 1700 455 Q1755 470 1765 630Z" fill="#66503c"/>
        </g>
        {/* street */}
        <path d="M0 690 L1920 650 V1080 H0Z" fill="url(#street)"/>
        <path d="M0 790 L1920 730" stroke="#7b8990" strokeWidth="5" opacity=".35"/>
        <path d="M0 970 L1920 850" stroke="#e9c28a" strokeWidth="5" opacity=".15"/>
        {/* glowing wet reflections */}
        <g filter="url(#blur)" opacity=".32">
          <path d="M1120 690 L1460 690 L1650 1080 H980Z" fill="#d98d57"/>
          <path d="M1550 700 L1780 700 L1910 1080 H1510Z" fill="#f2c17b"/>
          <path d="M250 800 L480 790 L620 1080 H190Z" fill="#7e9cb2"/>
        </g>
        <g opacity=".25">
          {Array.from({length:24},(_,i)=><path key={i} d={`M${980+i*35} ${760+(i%4)*20} l${-35+i%7*12} ${220+(i%3)*35}`} stroke="#f5c789" strokeWidth={4+i%4*2} />)}
        </g>
        {/* foreground passing car */}
        <g transform={`translate(${carX} 0)`} opacity=".88">
          <path d="M0 770 Q80 690 205 688 L390 715 Q455 730 490 800 L470 855 H20Z" fill="#172432" stroke="#0b1119" strokeWidth="12"/>
          <path d="M105 710 L190 650 H325 L390 720Z" fill="#8ba4b2" opacity=".5"/>
          <path d="M35 790 H455" stroke="#91aab8" strokeWidth="8" opacity=".4"/>
          <rect x="20" y="790" width="50" height="24" rx="8" fill="#f5d9a4"/><rect x="430" y="790" width="40" height="24" rx="8" fill="#df765c"/>
          <ellipse cx="105" cy="850" rx="52" ry="52" fill="#0b1117" stroke="#63717b" strokeWidth="10"/><ellipse cx="390" cy="850" rx="52" ry="52" fill="#0b1117" stroke="#63717b" strokeWidth="10"/>
        </g>
        {/* lamp posts */}
        <g><path d="M340 150V750" stroke="#111b25" strokeWidth="17"/><path d="M340 150 Q340 115 390 115" stroke="#111b25" strokeWidth="16" fill="none"/><circle cx="390" cy="125" r="75" fill="url(#lamp)" filter="url(#blur)"/><circle cx="390" cy="125" r="12" fill="#ffe0a5"/></g>
        {/* puddles */}
        <g fill="#93aebc" opacity={puddle}><ellipse cx="560" cy="1000" rx="210" ry="16"/><ellipse cx="1340" cy="920" rx="240" ry="14"/><ellipse cx="900" cy="1040" rx="300" ry="12"/></g>
        {/* character ground shadow */}
        <ellipse cx="790" cy="895" rx="155" ry="34" fill="#050b12" opacity=".5" filter="url(#shadow)"/>
        <Character frame={f} x={790} y={900} scale={1.04}/>
        {/* rain and foreground bokeh */}
        <Rain frame={f}/>
        <g opacity=".38" filter="url(#blur)"><circle cx="130" cy="400" r="36" fill="#d7b47d"/><circle cx="1780" cy="530" r="42" fill="#9ab7c5"/><circle cx="150" cy="850" r="28" fill="#e6b77a"/></g>
      </g>
      {/* film grain + vignette */}
      <defs><radialGradient id="vignette"><stop offset=".5" stopColor="#07101a" stopOpacity="0"/><stop offset="1" stopColor="#07101a" stopOpacity=".62"/></radialGradient></defs>
      <rect width="1920" height="1080" fill="url(#vignette)"/>
      <rect width="1920" height="1080" fill="#d6e1e8" opacity=".035"/>
    </svg>
    {/* directed camera overlays and typography */}
    <AbsoluteFill style={{pointerEvents:"none"}}>
      <div style={{position:"absolute",left:72,top:58,color:"#e9c58f",fontFamily:"Arial",fontWeight:800,letterSpacing:8,fontSize:22}}>WISE-LAB  /  ANIMATED STORY STUDY</div>
      <div style={{position:"absolute",left:74,bottom:76,width:Math.max(0,Math.min(1,(f-35)/45))*310,height:4,background:"#e7b675"}}/>
      <div style={{position:"absolute",right:72,bottom:64,color:"#f0e5d2",fontFamily:"Arial",fontSize:18,letterSpacing:4}}>01 — THE MOMENT AFTER</div>
      {f>210&&<div style={{position:"absolute",left:75,top:130,color:"#f3e7d4",fontFamily:"Georgia",fontSize:52,fontWeight:700,textShadow:"0 4px 18px #000"}}>Some moments follow you home.</div>}
      <div style={{position:"absolute",inset:24,border:"2px solid rgba(240,218,184,.26)",boxSizing:"border-box"}}/>
    </AbsoluteFill>
  </AbsoluteFill>;
}
export const PremiumShowcase=()=> <ShowcaseScene/>;
