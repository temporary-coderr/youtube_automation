import React from "react";
import {AbsoluteFill, Audio, Sequence, interpolate, useCurrentFrame, staticFile, Easing} from "remotion";
import {WISE_LAB_CAST} from "./wiseLabCast";
import {StoryStickerLayer} from "./StoryStickerLayer";
import {validateStoryShots} from "./storyRules";

/*
 * WISE-LAB — illustrated story film v2
 * Original layered editorial artwork, articulated character rigs, prop animation,
 * motivated camera movement and scene-specific blocking. No stock footage or paid APIs.
 */
const W = 1920, H = 1080;
const C = {
  ink:"#101821", paper:"#eee8dc", gold:"#e6b66f", warm:"#d58e5d",
  skin:"#b8785e", hair:"#17191f", hoodie:"#253447", denim:"#182332",
  light:"#f2dfbd", muted:"#8ea0a9"
};
const clamp = {extrapolateLeft:"clamp", extrapolateRight:"clamp"};
const ease = Easing.inOut(Easing.cubic);
const lerp = (f,a,b,x,y) => interpolate(f,[a,b],[x,y],{...clamp,easing:ease});
const pulse = (f,s=1) => (Math.sin(f*.12)*.5+.5)*s;

function CharacterRig({x=900,y=900,s=1,frame=0,kind="lead",action="idle",facing=1,walkAmount=0,talk=false}){
  const castId = kind === "friend" ? "maya" : kind;
  const profile = WISE_LAB_CAST[castId] || WISE_LAB_CAST.alex;
  const lead = castId === "alex";
  const skin = profile.skin;
  const skinShade = profile.skinShade;
  const shirt = profile.shirt;
  const pants = profile.pants;
  const hair = profile.hair;
  const gait = Math.sin(frame*.17);
  const walkTravel = walkAmount ? lerp(frame,0,119,0,176*walkAmount) : 0;
  const bob = walkAmount ? Math.abs(gait)*11 : Math.sin(frame*.055)*2.8;
  const stride = gait*walkAmount;
  const gestureWave = Math.sin(frame*.22)*19 + Math.sin(frame*.09)*7;
  const reach = lerp(frame,0,66,0,1);
  const armA = action==="gesture" ? -67+gestureWave : action==="reach" ? -132+reach*43+Math.sin(frame*.18)*5 : action==="phone" ? -104+Math.sin(frame*.1)*5 : action==="think" ? -43+Math.sin(frame*.08)*5 : stride*36;
  const armB = action==="gesture" ? 30+Math.sin(frame*.2+1)*15 : action==="reach" ? 18-reach*24 : action==="phone" ? -28+Math.sin(frame*.12)*6 : action==="think" ? -60+Math.sin(frame*.07)*5 : -stride*34;
  const bodyTurn = action==="turn" ? lerp(frame,0,100,-14,18) : action==="reach" ? lerp(frame,0,65,0,7) : action==="think" ? Math.sin(frame*.055)*3 : 0;
  const headTurn = action==="turn" ? lerp(frame,0,100,12,-14) : action==="think" ? 7+Math.sin(frame*.06)*3 : action==="phone" ? -8 : 0;
  const sit = action==="sit";
  const torsoDrop = sit ? 17+Math.sin(frame*.07)*2 : action==="reach" ? -3 : 0;
  const blink = (frame%97)>92 || (frame%149)>144;
  const mouth = talk && Math.sin(frame*.58)>0.04;
  const leftLeg = stride*29 + (sit?-18:0);
  const rightLeg = -stride*29 + (sit?24:0);
  return <g transform={"translate("+(x+walkTravel)+" "+(y+bob)+") scale("+s*(profile.scale || 1)*facing+" "+s*(profile.scale || 1)+")"}>
    <ellipse cx="0" cy="-2" rx="106" ry="20" fill="#070c12" opacity=".42"/>
    {/* Legs: layered denim, seams, knees and sneakers */}
    <g transform={"rotate("+leftLeg+" -37 -150)"}>
      <path d="M-55 -180 Q-68 -108 -46 -34 L-40 -4 Q-27 9 5 2 L9 -22 L-6 -110 L-4 -184Z" fill={pants}/>
      <path d="M-44 -30 Q-20 -43 7 -23 L18 4 Q14 17 -45 13 L-57 1Z" fill="#0c131d"/>
      <path d="M-55 2 Q-20 -8 13 5 L24 20 Q-6 33 -76 22 Q-86 11 -55 2Z" fill="#111820"/>
      <path d="M-48 -150 L-37 -49 M-52 -92 L-8 -88 M-45 -42 L-15 -37" stroke="#455568" strokeWidth="3.5" opacity=".8" fill="none"/>
      <path d="M-50 -22 Q-26 -30 -4 -19" stroke="#647284" strokeWidth="3" fill="none" opacity=".6"/>
      <path d="M-65 13 Q-28 23 13 14" stroke="#77818a" strokeWidth="3" fill="none" opacity=".65"/>
      <path d="M-65 16 Q-78 13 -83 24 Q-81 35 -40 36 L19 30 Q27 24 15 17" fill="#202a32" stroke="#0b1118" strokeWidth="4"/>
      <path d="M-59 24 L-20 26 M-48 31 L-12 30" stroke="#a9b3b8" strokeWidth="3" opacity=".8"/>
    </g>
    <g transform={"rotate("+rightLeg+" 34 -150)"}>
      <path d="M8 -181 Q28 -110 23 -42 L38 -3 Q52 9 78 0 L77 -23 L62 -112 L61 -185Z" fill={pants}/>
      <path d="M34 -34 Q55 -42 79 -21 L88 4 Q75 17 29 12 L22 -3Z" fill="#0c131d"/>
      <path d="M29 3 Q60 -8 88 4 L98 19 Q67 34 17 22 Q10 11 29 3Z" fill="#111820"/>
      <path d="M60 -151 L66 -55 M32 -90 L72 -86 M42 -42 L75 -37" stroke="#455568" strokeWidth="3.5" opacity=".8" fill="none"/>
      <path d="M27 -22 Q53 -30 78 -18" stroke="#647284" strokeWidth="3" fill="none" opacity=".6"/>
      <path d="M18 14 Q56 26 94 14" stroke="#77818a" strokeWidth="3" fill="none" opacity=".65"/>
      <path d="M20 17 Q10 13 6 25 Q9 36 47 36 L102 30 Q110 24 98 17" fill="#202a32" stroke="#0b1118" strokeWidth="4"/>
      <path d="M32 24 L70 26 M42 31 L78 30" stroke="#a9b3b8" strokeWidth="3" opacity=".8"/>
    </g>
    {/* Hoodie torso with hood, pocket, ribbing and fabric folds */}
    <g transform={"translate(0 "+torsoDrop+") rotate("+bodyTurn+" 0 -340)"}>
      <path d="M-75 -395 Q-92 -435 -45 -448 Q0 -465 45 -448 Q92 -435 75 -395 L54 -363 H-54Z" fill="#182636" stroke="#111b27" strokeWidth="7"/>
      <path d="M-87 -390 Q-116 -360 -105 -278 L-84 -177 Q-2 -151 84 -177 L106 -278 Q116 -361 87 -390 Q42 -420 0 -415 Q-46 -420 -87 -390Z" fill={shirt} stroke="#172332" strokeWidth="5"/>
      <path d="M-64 -374 Q-48 -403 0 -403 Q48 -403 64 -374 L44 -310 Q0 -286 -44 -310Z" fill="#172638"/>
      <path d="M-27 -398 L0 -345 L27 -398" stroke="#8291a0" strokeWidth="5" fill="none" opacity=".75"/>
      <path d="M-75 -327 Q-39 -298 0 -302 Q44 -298 75 -327" stroke="#53677d" strokeWidth="4" fill="none" opacity=".65"/>
      <path d="M-15 -335 L-19 -270 M15 -335 L19 -270" stroke="#c1b29d" strokeWidth="4" strokeLinecap="round"/>
      <circle cx="-19" cy="-267" r="5" fill="#d3c4aa"/><circle cx="19" cy="-267" r="5" fill="#d3c4aa"/>
      <path d="M-73 -245 Q0 -222 73 -245" stroke="#101c2a" strokeWidth="5" opacity=".55" fill="none"/>
      <path d="M-48 -244 Q0 -220 48 -244 L40 -199 Q0 -183 -40 -199Z" fill="#1a2a3c" stroke="#40546a" strokeWidth="4"/>
      <path d="M-38 -232 Q0 -216 38 -232" stroke="#65798b" strokeWidth="3" fill="none"/>
      <path d="M-82 -365 Q-110 -345 -106 -286 M81 -365 Q110 -345 106 -286" stroke="#566a7e" strokeWidth="7" fill="none" opacity=".65"/>
      <path d="M-91 -278 L-80 -226 M91 -278 L80 -226" stroke="#192737" strokeWidth="8" fill="none"/>
      <path d="M-85 -190 Q0 -171 85 -190" stroke="#111b28" strokeWidth="10" fill="none"/>
      <path d="M-71 -355 Q-53 -338 -46 -320 M70 -355 Q52 -338 45 -320" stroke="#8290a0" strokeWidth="3" fill="none" opacity=".35"/>
      <path d="M-55 -285 l20 15 M55 -285 l-20 15" stroke="#9ba6af" strokeWidth="3" opacity=".28"/>
    </g>
    {/* Arms with shoulder folds, cuffs, forearms and articulated fingers */}
    <g transform={"rotate("+armA+" -82 -358)"}>
      <path d="M-82 -358 Q-122 -320 -112 -262 L-101 -220" stroke={shirt} strokeWidth="51" strokeLinecap="round" fill="none"/>
      <path d="M-107 -337 Q-125 -298 -116 -267" stroke="#52677e" strokeWidth="5" fill="none" opacity=".8"/>
      <path d="M-116 -267 L-103 -220" stroke="#697b8d" strokeWidth="7" fill="none" opacity=".75"/>
      <path d="M-101 -224 Q-95 -200 -82 -185" stroke={skin} strokeWidth="29" strokeLinecap="round" fill="none"/>
      <path d="M-95 -210 Q-88 -197 -81 -190" stroke={skinShade} strokeWidth="4" fill="none" opacity=".7"/>
      <path d="M-91 -188 Q-71 -188 -69 -170 Q-76 -157 -95 -169 Q-109 -180 -91 -188Z" fill={skin}/>
      <path d="M-84 -181 Q-74 -177 -72 -166 M-94 -178 Q-101 -168 -95 -160 M-82 -187 L-77 -180" stroke={skinShade} strokeWidth="3" strokeLinecap="round" fill="none"/>
      <path d="M-108 -227 L-98 -215" stroke="#a9b5bf" strokeWidth="4" opacity=".55"/>
    </g>
    <g transform={"rotate("+armB+" 82 -358)"}>
      <path d="M82 -358 Q122 -320 112 -262 L101 -220" stroke={shirt} strokeWidth="51" strokeLinecap="round" fill="none"/>
      <path d="M107 -337 Q125 -298 116 -267" stroke="#52677e" strokeWidth="5" fill="none" opacity=".8"/>
      <path d="M116 -267 L103 -220" stroke="#697b8d" strokeWidth="7" fill="none" opacity=".75"/>
      <path d="M101 -224 Q95 -200 82 -185" stroke={skin} strokeWidth="29" strokeLinecap="round" fill="none"/>
      <path d="M95 -210 Q88 -197 81 -190" stroke={skinShade} strokeWidth="4" fill="none" opacity=".7"/>
      <path d="M91 -188 Q71 -188 69 -170 Q76 -157 95 -169 Q109 -180 91 -188Z" fill={skin}/>
      <path d="M84 -181 Q74 -177 72 -166 M94 -178 Q101 -168 95 -160 M82 -187 L77 -180" stroke={skinShade} strokeWidth="3" strokeLinecap="round" fill="none"/>
      <path d="M108 -227 L98 -215" stroke="#a9b5bf" strokeWidth="4" opacity=".55"/>
    </g>
    {/* Neck and detailed head */}
    <g transform={"translate(0 -465) rotate("+headTurn+")"}>
      <path d="M-24 -63 L-24 -103 L24 -103 L24 -61 Q0 -42 -24 -63Z" fill={skinShade}/>
      <path d="M-66 -16 Q-69 -100 -24 -127 Q28 -147 65 -88 Q82 -54 55 30 Q33 73 -16 67 Q-61 51 -66 -16Z" fill={skin} stroke="#754a3e" strokeWidth="3"/>
      <path d="M-48 21 Q-20 47 16 43 Q42 37 54 5 Q42 59 2 66 Q-39 62 -48 21Z" fill={skinShade} opacity=".25"/>
      <path d="M-66 -31 Q-94 -112 -38 -150 Q12 -184 62 -142 Q94 -113 71 -62 L49 -83 Q22 -69 -5 -83 Q-26 -97 -51 -49Z" fill={hair}/>
      {lead ? <>
        <path d="M-57 -86 Q-76 -137 -32 -164 Q-3 -184 29 -168 Q-7 -157 5 -130 Q-22 -119 -57 -86Z" fill="#202631"/>
        <path d="M-56 -114 Q-51 -154 -12 -163 M-29 -126 Q-6 -155 22 -151 M10 -133 Q34 -153 54 -127" stroke="#39404a" strokeWidth="5" fill="none" strokeLinecap="round" opacity=".8"/>
        <path d="M-64 -81 Q-79 -104 -63 -132 M50 -125 Q77 -112 72 -81" stroke="#0e131a" strokeWidth="8" fill="none" strokeLinecap="round"/>
      </> : <>
        <path d="M-58 -75 Q-80 -121 -40 -160 Q12 -190 56 -143 Q88 -106 62 -48 L46 43 Q38 16 34 -39 Q-5 -14 -53 -36Z" fill="#211b1a"/>
        <path d="M-47 -119 Q-25 -160 9 -162 M5 -143 Q34 -163 57 -132" stroke="#49352e" strokeWidth="5" fill="none"/>
      </>}
      {profile.silhouette === "short-curl" && <g fill={hair}>
        {[-42,-22,0,22,42].map((cx,i)=><circle key={i} cx={cx} cy={-133-(i%2)*9} r="18"/>)}
      </g>}
      {profile.silhouette === "curly-bob" && <g fill={hair}>
        {[-62,-48,48,62].map((cx,i)=><circle key={i} cx={cx} cy={-67+(i%2)*24} r="16"/>)}
      </g>}
      {profile.silhouette === "child-curly" && <g fill={hair}>
        {[-42,-22,0,22,42].map((cx,i)=><circle key={i} cx={cx} cy={-143-(i%2)*7} r="17"/>)}
      </g>}
      {profile.silhouette === "silver-side-part" && <path d="M-53 -116 Q-24 -165 20 -153 Q43 -148 61 -124" stroke="#e0ded5" strokeWidth="8" fill="none" strokeLinecap="round"/>}
      <path d="M-56 -17 Q-72 -22 -67 4 Q-60 26 -48 18" fill={skinShade}/>
      <path d="M56 -17 Q72 -22 67 4 Q60 26 48 18" fill={skinShade}/>
      <path d="M-39 -22 Q-23 -34 -7 -24 M12 -24 Q29 -35 43 -21" stroke="#34241f" strokeWidth="8" fill="none" strokeLinecap="round"/>
      {blink ? <>
        <path d="M-35 0 Q-22 8 -9 0 M12 0 Q27 8 40 0" stroke="#2b1d19" strokeWidth="5" fill="none" strokeLinecap="round"/>
      </> : <>
        <ellipse cx="-22" cy="0" rx="10" ry="9" fill="#f4e8d7"/><ellipse cx="26" cy="0" rx="10" ry="9" fill="#f4e8d7"/>
        <ellipse cx="-20" cy="1" rx="5" ry="6" fill="#624b39"/><ellipse cx="27" cy="1" rx="5" ry="6" fill="#624b39"/>
        <circle cx="-20" cy="1" r="3" fill="#171719"/><circle cx="27" cy="1" r="3" fill="#171719"/>
        <circle cx="-21" cy="-2" r="2" fill="#fff"/><circle cx="26" cy="-2" r="2" fill="#fff"/>
        <path d="M-34 -8 Q-22 -14 -10 -8 M14 -8 Q27 -14 39 -8" stroke="#17191d" strokeWidth="3" fill="none"/>
      </>}
      <path d="M1 3 Q-8 26 2 29 Q8 31 11 26" stroke="#8e5a49" strokeWidth="4" fill="none" strokeLinecap="round"/>
      <path d="M-2 28 Q4 32 10 27" stroke="#d79a7b" strokeWidth="2" fill="none" opacity=".65"/>
      <ellipse cx="-39" cy="30" rx="13" ry="7" fill="#d88c78" opacity=".16"/><ellipse cx="40" cy="30" rx="13" ry="7" fill="#d88c78" opacity=".16"/>
      {mouth ? <path d="M-7 45 Q4 37 17 46 Q14 61 4 61 Q-6 59 -7 45Z" fill="#502d2b" stroke="#713d37" strokeWidth="2"/> : <path d="M-12 45 Q4 54 19 43" stroke="#713d37" strokeWidth="4" fill="none" strokeLinecap="round"/>}
      {profile.ageStyle === "elder" && <g fill={hair} opacity=".92"><path d="M-37 54 Q0 76 37 54 Q30 105 0 106 Q-30 105 -37 54Z"/><path d="M-39 56 Q-27 49 -17 58 M17 58 Q27 49 39 56" stroke="#777d7b" strokeWidth="3" fill="none"/></g>}
      {lead && <path d="M-46 -112 Q-21 -128 -2 -115 M8 -122 Q34 -137 53 -106" stroke="#11151c" strokeWidth="12" fill="none" strokeLinecap="round"/>}
      <path d="M-17 70 Q0 78 20 68" stroke="#754b40" strokeWidth="3" fill="none" opacity=".55"/>
    </g>
    {/* Small recurring costume accents */}
    {lead && <g>
      <path d="M-49 -408 Q0 -434 49 -408" stroke="#8ea0ae" strokeWidth="5" fill="none" opacity=".65"/>
      <path d="M-80 -369 l-13 17 M80 -369 l13 17" stroke="#a8b3bc" strokeWidth="3" opacity=".55"/>
    </g>}
  </g>;
}
function CafeSet({frame=0}){
  const rain = Array.from({length:34},(_,i)=><path key={i} d={"M"+(105+i*49)+" "+(140+(i*37)%450)+" l-12 35"} transform={"translate(0 "+((frame*7+i*13)%62)+")"} stroke="#b6d4e2" strokeWidth="3" opacity=".45"/>);
  const steam = i => <path d={"M"+(i*45-12)+" "+(770-(frame%55)*.45)+" q-24 -28 0 -53 q20 -23 0 -46"} stroke="#f0d9b7" strokeWidth="5" fill="none" opacity={.32+Math.sin(frame*.09+i)*.12}/>;
  return <g>
    <rect width={W} height={H} fill="#24323a"/>
    <rect y="0" width={W} height="740" fill="#3b4545"/>
    <path d="M0 0 H1920 V115 Q1500 160 960 116 T0 115Z" fill="#2a3031"/>
    <path d="M0 740 H1920 V1080 H0Z" fill="#49382e"/>
    <path d="M0 920 L1920 820 V1080 H0Z" fill="#6b4c39" opacity=".6"/>
    <g>
      <rect x="105" y="100" width="700" height="535" rx="12" fill="#172631" stroke="#b58b67" strokeWidth="22"/>
      <rect x="129" y="124" width="652" height="487" fill="#526f7e"/>
      <rect x="129" y="124" width="652" height="487" fill="#263c52" opacity=".18"/>
      {[0,1,2,3,4].map(i=><g key={i}><rect x={160+i*133} y={320-(i%2)*65} width="84" height={290+(i%2)*65} fill={["#34485a","#2b3d51","#52606a","#273849","#56636c"][i]}/><rect x={171+i*133} y={350-(i%2)*65} width="18" height="10" fill="#e9bd83" opacity=".65"/><rect x={207+i*133} y={410-(i%2)*65} width="18" height="10" fill="#e9bd83" opacity=".42"/></g>)}
      <path d="M455 124 V611 M129 385 H781" stroke="#b58b67" strokeWidth="18"/>
      {rain}
      <path d="M125 615 Q450 580 785 615" stroke="#e1c29c" strokeWidth="6" fill="none" opacity=".5"/>
    </g>
    <g opacity=".9">
      <rect x="915" y="130" width="760" height="355" fill="#344247"/>
      <rect x="940" y="155" width="710" height="305" fill="#1e2c34"/>
      {[0,1,2,3,4,5,6].map(i=><g key={i}><rect x={970+i*92} y={188+(i%3)*28} width="55" height={140+(i%3)*22} rx="4" fill={i%2?"#6b5441":"#98744c"} opacity=".75"/><rect x={978+i*92} y={204+(i%3)*28} width="39" height="35" fill="#d4ad78" opacity=".45"/></g>)}
      <path d="M920 500 H1680" stroke="#a77d58" strokeWidth="24"/>
    </g>
    <g>
      {[430,1040,1570].map((x,i)=><g key={i}><path d={"M"+x+" 0 V"+(170+i*30)} stroke="#2a2523" strokeWidth="7"/><path d={"M"+(x-38)+" "+(160+i*30)+" Q"+x+" "+(110+i*30)+" "+(x+38)+" "+(160+i*30)+" L"+(x+25)+" "+(195+i*30)+" H"+(x-25)+"Z"} fill="#d49a59"/><ellipse cx={x} cy={190+i*30} rx="56" ry="18" fill="#f4c982" opacity=".24"/></g>)}
    </g>
    <g>
      <rect x="35" y="610" width="120" height="220" fill="#293b35"/><path d="M95 640 Q20 530 58 466 Q130 515 95 640 M95 640 Q178 515 156 458 Q94 496 95 640 M96 640 Q-5 586 12 530 Q80 545 96 640" fill="#536b53"/><rect x="80" y="635" width="30" height="170" fill="#725340"/>
      <rect x="1760" y="610" width="110" height="220" fill="#293b35"/><path d="M1815 650 Q1740 530 1778 466 Q1850 515 1815 650 M1815 650 Q1895 520 1875 465 Q1810 496 1815 650" fill="#536b53"/><rect x="1800" y="635" width="30" height="170" fill="#725340"/>
    </g>
    <path d="M0 825 Q500 770 960 824 T1920 810 V1080 H0Z" fill="#4b372c"/>
    <path d="M0 923 Q550 865 1100 930 T1920 905" stroke="#8a6242" strokeWidth="5" fill="none" opacity=".5"/>
    <g opacity=".5">{[0,1,2,3,4,5].map(i=><path key={i} d={"M"+(i*360+50)+" 940 l-170 140"} stroke="#c19b72" strokeWidth="3"/>)}</g>
    {steam(0)}{steam(1)}{steam(2)}
  </g>;
}

function BedroomSet({frame=0,dawn=false}){
  const sky = dawn ? "#b68a70" : "#1c3046";
  return <g>
    <rect width={W} height={H} fill={dawn?"#b39a85":"#202e3c"}/>
    <rect x="0" y="0" width={W} height="760" fill={dawn?"#665c58":"#263747"}/>
    <path d="M0 760 Q500 700 1000 770 T1920 735 V1080 H0Z" fill="#44352e"/>
    <rect x="1240" y="95" width="500" height="520" rx="8" fill="#152130" stroke="#8e7967" strokeWidth="20"/>
    <rect x="1260" y="115" width="460" height="480" fill={sky}/>
    {[0,1,2,3,4,5,6,7].map(i=><g key={i}><rect x={1272+i*59} y={dawn?300+(i%3)*60:230+(i%3)*60} width="44" height={340-(i%3)*26} fill={dawn?"#564b4a":"#172b3e"}/><rect x={1280+i*59} y={dawn?360+(i%3)*60:276+(i%3)*60} width="13" height="10" fill="#eebf79" opacity=".75"/></g>)}
    <circle cx={dawn?1510:1620} cy={dawn?225:190} r={dawn?65:38} fill={dawn?"#f8d39a":"#e2e4d9"} opacity=".9"/>
    <path d="M1490 115 V595 M1260 350 H1720" stroke="#8e7967" strokeWidth="16"/>
    <g>
      <rect x="115" y="120" width="360" height="270" fill="#1b2a38" stroke="#8a765e" strokeWidth="13"/>
      <rect x="130" y="135" width="330" height="240" fill="#334753"/>
      <path d="M170 333 L250 225 L310 284 L365 183 L433 333Z" fill="#71837c" opacity=".55"/>
      <path d="M230 135 V375 M350 135 V375" stroke="#a58a6c" strokeWidth="5"/>
    </g>
    <g>
      <rect x="270" y="770" width="980" height="26" rx="8" fill="#8d674b"/>
      <path d="M320 796 L300 1080 M1200 796 L1220 1080" stroke="#49372d" strokeWidth="25"/>
      <rect x="355" y="712" width="365" height="58" rx="10" fill="#1b2938"/>
      <rect x="375" y="726" width="324" height="36" rx="8" fill="#6d7d83"/>
      <rect x="765" y="694" width="200" height="75" rx="9" fill="#111b26"/>
      <rect x="777" y="704" width="176" height="57" rx="6" fill="#41637a"/>
      <path d="M804 747 Q857 710 927 744" stroke="#b7cfda" strokeWidth="4" fill="none" opacity=".55"/>
      <rect x="1000" y="720" width="130" height="48" rx="7" fill="#9b7956"/>
      <path d="M1012 720 L1030 650 H1090 L1120 720Z" fill="#c69a68"/>
    </g>
    <g>
      <path d="M1100 720 L1140 570 Q1175 530 1208 570 L1250 720Z" fill="#d7a96e"/>
      <path d="M1148 575 Q1175 520 1200 575" stroke="#f1d09a" strokeWidth="9" fill="none"/>
      <rect x="1168" y="714" width="17" height="55" fill="#c89a68"/>
      <ellipse cx="1177" cy="778" rx="78" ry="11" fill="#b68a5a"/>
    </g>
    <g>
      <rect x="1450" y="700" width="360" height="270" rx="8" fill="#36423f"/>
      <rect x="1470" y="715" width="320" height="210" rx="8" fill="#5c6460"/>
      <path d="M1470 860 Q1570 790 1640 860 T1790 830 V925 H1470Z" fill="#a68a6d"/>
      <rect x="1425" y="950" width="410" height="35" fill="#242e2e"/>
    </g>
    <g>
      <rect x="80" y="650" width="140" height="150" fill="#6d523d"/>
      <path d="M150 650 Q68 575 110 505 Q189 540 150 650 M150 650 Q232 568 211 500 Q143 534 150 650" fill="#53705c"/>
      <path d="M150 650 Q75 620 75 570 Q135 577 150 650" fill="#69805e"/>
    </g>
    <g opacity=".55">
      {[0,1,2,3,4,5].map(i=><path key={i} d={"M"+(90+i*270)+" "+(1010-(i%2)*20)+" l180 -18"} stroke="#92725a" strokeWidth="4"/>)}
    </g>
    {!dawn && <g opacity=".35">{Array.from({length:16},(_,i)=><circle key={i} cx={(i*137+frame*0.5)%1900} cy={180+(i*79)%590} r="2.5" fill="#f1d9ae"/>)}</g>}
  </g>;
}

function StreetSet({frame=0}){
 return <g>
  <rect width={W} height={H} fill="#33404a"/>
  <rect width={W} height="730" fill="#52616a"/>
  {[0,1,2,3,4,5].map(i=><g key={i}><path d={"M"+(i*345-40)+" 210 L"+(i*345+295)+" 190 L"+(i*345+320)+" 770 L"+(i*345-10)+" 790Z"} fill={["#435663","#394b59","#5b6669"][i%3]}/><rect x={i*345+35} y="260" width="78" height="120" fill="#273b4b"/><rect x={i*345+150} y="260" width="86" height="120" fill="#283d4c"/><rect x={i*345+35} y="430" width="78" height="125" fill="#253948"/><rect x={i*345+150} y="430" width="86" height="125" fill="#253948"/></g>)}
  <path d="M0 740 L1920 670 V1080 H0Z" fill="#2c3337"/>
  <path d="M800 1080 L950 720 L1030 720 L1170 1080" fill="#5a6261"/>
  <path d="M0 940 Q700 860 1920 900" stroke="#b6a58f" strokeWidth="6" opacity=".35" fill="none"/>
  <g opacity=".75"><rect x="300" y="610" width="16" height="180" fill="#202a30"/><path d="M308 615 Q235 585 240 525 Q314 540 308 615 M308 615 Q375 565 367 510 Q302 535 308 615" fill="#526e5f"/><rect x="1650" y="570" width="18" height="210" fill="#202a30"/><path d="M1658 575 Q1580 520 1602 460 Q1680 495 1658 575 M1658 575 Q1730 510 1710 450 Q1640 490 1658 575" fill="#536d5e"/></g>
  {[0,1,2,3,4,5,6,7,8].map(i=><g key={i} opacity=".55"><path d={"M"+(i*235+40)+" 0 V"+(50+(i%3)*24)} stroke="#1e252a" strokeWidth="3"/><circle cx={i*235+40} cy={66+(i%3)*24} r="5" fill="#f0c17e"/></g>)}
  <g opacity=".28">{Array.from({length:24},(_,i)=><path key={i} d={"M"+(i*86+12)+" "+(190+(i*47)%490)+" l-10 32"} stroke="#e6edf0" strokeWidth="2"/>)}</g>
 </g>;
}

function ParkSet({frame=0}){
 return <g>
  <rect width={W} height={H} fill="#9daea2"/>
  <rect width={W} height="650" fill="#aac0b2"/>
  <circle cx="1480" cy="200" r="110" fill="#f4d7a2"/>
  <path d="M0 620 Q340 500 700 620 T1440 585 T1920 625 V1080 H0Z" fill="#728e77"/>
  <path d="M0 760 Q450 660 900 760 T1920 715 V1080 H0Z" fill="#3f6653"/>
  <path d="M620 1080 Q860 810 1000 700 Q1150 860 1420 1080Z" fill="#b8a58b"/>
  <path d="M760 1080 Q950 820 1010 725 Q1110 860 1270 1080Z" fill="#cdbb9c"/>
  {[0,1,2,3,4,5,6,7].map(i=><g key={i} transform={"translate("+(i*270-80)+" "+(160+(i%2)*70)+")"}><rect x="65" y="220" width="28" height="390" fill="#665341"/><path d="M80 235 Q-30 115 20 10 Q100 -58 168 45 Q215 158 80 235Z" fill={i%2?"#5b795c":"#688363"}/><path d="M80 208 Q-48 110 -18 38 Q72 4 126 84 Q160 150 80 208Z" fill="#79936b" opacity=".55"/></g>)}
  <g opacity=".9">
   <rect x="1420" y="605" width="18" height="185" fill="#4c4c40"/><path d="M1330 620 Q1428 560 1525 620 L1502 646 H1352Z" fill="#394c43"/><path d="M1350 647 H1505" stroke="#d8c49d" strokeWidth="8"/>
   <rect x="160" y="700" width="210" height="14" rx="7" fill="#4e473d"/><path d="M180 712 L170 780 M350 712 L365 780" stroke="#4e473d" strokeWidth="13"/>
  </g>
  <g opacity=".6">{Array.from({length:40},(_,i)=><ellipse key={i} cx={(i*193+frame*.18)%1940} cy={500+(i*41)%330} rx="9" ry="4" fill={i%2?"#d4c68e":"#e7d5a8"} transform={"rotate("+(i*17)+" "+((i*193+frame*.18)%1940)+" "+(500+(i*41)%330)+")"}/>)}</g>
  <path d="M0 900 Q400 850 760 900 T1500 880 T1920 920 V1080 H0Z" fill="#315541"/>
 </g>;
}

function Cup({x,y,steam=true,frame=0}){
 return <g transform={"translate("+x+" "+y+")"}>
   <ellipse cx="0" cy="0" rx="42" ry="11" fill="#d5c7b6"/>
   <path d="M-37 -4 L-30 45 Q0 61 30 45 L37 -4Z" fill="#eee4d6"/>
   <path d="M31 4 Q70 -5 61 27 Q55 46 31 39" stroke="#e7ddd0" strokeWidth="10" fill="none"/>
   <ellipse cx="0" cy="-4" rx="37" ry="9" fill="#513b2d"/>
   <ellipse cx="0" cy="-7" rx="23" ry="5" fill="#806047" opacity=".65"/>
   {steam && <g opacity=".45">{[0,1,2].map(i=><path key={i} d={"M"+(i*15-12)+" -18 q-18 -24 0 -45 q16 -19 0 -36"} stroke="#fff0d9" strokeWidth="4" fill="none" transform={"translate(0 "+(-Math.sin(frame*.08+i)*4)+")"}/>)}</g>}
 </g>;
}

function Phone({x,y,frame=0,tilt=0,screen=true,glow=false}){
 return <g transform={"translate("+x+" "+y+") rotate("+tilt+")"}>
  <rect x="-56" y="-112" width="112" height="224" rx="18" fill="#090f17" stroke="#87939a" strokeWidth="6"/>
  <rect x="-47" y="-101" width="94" height="202" rx="11" fill={screen?"#233b52":"#111923"}/>
  {screen && <>
   <rect x="-31" y="-78" width="62" height="7" rx="3" fill="#d1dce1" opacity=".5"/>
   <circle cx="0" cy="-35" r="20" fill="#e8bb75" opacity=".9"/>
   <rect x="-31" y="7" width="60" height="10" rx="5" fill="#b9c8ce" opacity=".62"/>
   <rect x="-31" y="28" width="46" height="8" rx="4" fill="#b9c8ce" opacity=".35"/>
   <rect x="-31" y="52" width="62" height="8" rx="4" fill="#b9c8ce" opacity=".35"/>
  </>}
  <circle cx="0" cy="91" r="4" fill="#a9b5bd"/>
  {glow && <rect x="-50" y="-105" width="100" height="210" rx="14" fill="#f0bd71" opacity={.08+.08*pulse(frame)}/>}
 </g>;
}

function CafeForeground({frame=0,alone=false}){
 return <g>
  <path d="M520 775 Q960 705 1450 780 L1510 845 Q970 795 470 850Z" fill="#765239"/>
  <path d="M470 850 Q960 798 1510 845 L1500 885 Q960 850 490 895Z" fill="#b18154"/>
  <path d="M550 875 L530 1080 M1430 874 L1450 1080" stroke="#51392c" strokeWidth="32"/>
  <path d="M740 845 L730 1050 M1255 855 L1270 1050" stroke="#66442f" strokeWidth="22"/>
  <Cup x={alone?1080:940} y={766} frame={frame}/>
  {!alone && <Cup x={1210} y={777} frame={frame+12}/>}
  <rect x="1010" y="736" width="150" height="11" rx="5" fill="#d8c5a4" opacity=".7"/>
  <path d="M1050 745 Q1070 705 1110 718" stroke="#e6d5b8" strokeWidth="4" fill="none" opacity=".6"/>
 </g>;
}

function DeskProps({frame=0,phone=true,faceDown=false}){
 return <g>
  <rect x="295" y="755" width="1000" height="27" rx="8" fill="#8f6849"/>
  <path d="M350 782 L330 1080 M1240 782 L1260 1080" stroke="#4b392f" strokeWidth="28"/>
  <rect x="550" y="665" width="370" height="90" rx="12" fill="#111c29"/>
  <rect x="568" y="678" width="334" height="62" rx="7" fill="#31516a"/>
  <rect x="690" y="752" width="90" height="13" fill="#8b9699"/>
  <path d="M570 716 Q670 665 770 718 T897 705" stroke="#9fbdc7" strokeWidth="4" fill="none" opacity=".45"/>
  <g transform="translate(1075 0)">
   <path d="M0 750 L38 574 Q70 542 102 574 L142 750Z" fill="#d6a66c"/>
   <path d="M36 578 Q70 529 103 578" stroke="#f3d4a0" strokeWidth="10" fill="none"/>
   <rect x="62" y="744" width="18" height="28" fill="#c79963"/>
   <ellipse cx="70" cy="778" rx="96" ry="10" fill="#bc8d5e"/>
  </g>
  <rect x="930" y="714" width="110" height="38" rx="5" fill="#b9a286"/>
  <path d="M950 725 H1020 M950 736 H1010" stroke="#75634f" strokeWidth="4"/>
  <Cup x={460} y={748} frame={frame}/>
  {phone && <Phone x={(faceDown?1130:1190)+Math.sin(frame*.75)*3} y={faceDown?722:680+Math.sin(frame*.55)*2} frame={frame} tilt={faceDown?lerp(frame,0,46,0,82):lerp(frame,0,119,-8,8)} screen={!faceDown || frame<38} glow={!faceDown && pulse(frame)>.25}/>} 
  <g opacity=".8"><rect x="375" y="620" width="80" height="92" rx="5" fill="#7b5a3d"/><path d="M387 638 H443 M387 651 H437 M387 664 H430" stroke="#d9c3a0" strokeWidth="4"/></g>
 </g>;
}

function MemoryPanel({x=1230,y=265,frame=0,opacity=1}){
 return <g opacity={opacity} transform={"translate("+x+" "+(y+Math.sin(frame*.06)*7)+")"}>
  <rect x="-4" y="0" width="330" height="205" rx="12" fill="#111a25" opacity=".76" stroke="#e0c49a" strokeWidth="3"/>
  <rect x="10" y="15" width="302" height="175" rx="7" fill="#6d7777"/>
  <path d="M10 133 L74 72 L120 112 L166 54 L228 110 L312 74 V190 H10Z" fill="#405a60"/>
  <g transform="translate(115 165) scale(.33)"><CharacterRig x={0} y={0} s={1} frame={frame} kind="lead" action="gesture"/></g>
  <circle cx="267" cy="42" r="19" fill="#e8b66e"/><path d="M261 42 L267 48 L278 34" stroke="#27333a" strokeWidth="4" fill="none"/>
 </g>;
}

function NotificationStack({frame=0}){
 return <g opacity={.9}>
  {[0,1,2].map(i=>{
    const y=320+i*102+Math.sin(frame*.08+i)*5;
    const alpha=interpolate(frame,[i*12,i*12+12,93,119],[0,1,1,0],clamp);
    return <g key={i} opacity={alpha} transform={"translate(1360 "+y+")"}>
      <rect width="380" height="76" rx="15" fill="#edf0ed" opacity=".95"/>
      <circle cx="39" cy="38" r="21" fill={i===0?"#c98b63":i===1?"#728f86":"#7b8aa0"}/>
      <rect x="77" y="21" width="180" height="9" rx="4" fill="#40515b"/>
      <rect x="77" y="39" width="250" height="7" rx="3" fill="#8a999c"/>
      <circle cx="347" cy="24" r="5" fill="#d37d61"/>
    </g>;
  })}
 </g>;
}

function ThoughtLoop({frame=0}){
 const rot=frame*1.2;
 return <g transform={"translate(1410 365)"}>
   <circle cx="0" cy="0" r="148" fill="none" stroke="#e6c18c" strokeWidth="5" strokeDasharray="12 18" opacity=".38" transform={"rotate("+rot+")"}/>
   <circle cx="0" cy="0" r="103" fill="none" stroke="#e6c18c" strokeWidth="3" opacity=".22"/>
   <g transform={"rotate("+(-rot*1.6)+")"}>
    {[0,1,2,3].map(i=><g key={i} transform={"rotate("+(i*90)+") translate(0 -145)"}>
      <circle r="27" fill="#e7c89e" opacity=".75"/><path d="M-13 5 Q0 -14 13 5 Q0 18 -13 5Z" fill="#4d5b5b"/>
    </g>)}
   </g>
   <path d="M82 -123 L109 -115 L92 -91" stroke="#e9c996" strokeWidth="8" fill="none" strokeLinecap="round"/>
 </g>;
}

function ParkBirds({frame=0}){
 return <g fill="#344b43" opacity=".7">
  {[0,1,2].map(i=><path key={i} d={"M"+(920+i*72+Math.sin(frame*.09+i)*12)+" "+(220+i*18)+" q18 -16 36 0 q18 -16 36 0"} stroke="#344b43" strokeWidth="5" fill="none" strokeLinecap="round"/>)}
 </g>;
}

const shots = [
 {place:"cafe",title:"THE MOMENT",caption:"A tiny awkward moment happens.",lead:{x:755,y:925,action:"gesture",talk:true},friend:{x:1390,y:930,action:"idle",talk:false},sticker:{type:"tag",text:"A MOMENT EVERYONE KNOWS",tone:"gold"},zoom:[1.0,1.055],pan:[0,-20]},
 {place:"cafe",title:"THE PAUSE",caption:"A pause lasts only a second.",lead:{x:765,y:925,action:"gesture",talk:true},friend:{x:1390,y:930,action:"turn",talk:true},zoom:[1.055,1.11],pan:[-20,-70],bubble:true},
 {place:"cafe",title:"THE EXIT",caption:"Then the other person moves on.",lead:{x:735,y:925,action:"idle"},friend:{x:0,y:930,action:"walk",walk:1,leave:true},zoom:[1.11,1.04],pan:[-70,40]},
 {place:"cafe-alone",title:"THE REPLAY",caption:"But your mind keeps the moment.",lead:{x:760,y:925,action:"think"},sticker:{type:"definition",term:"Rumination",text:"When the mind repeatedly circles the same thought without moving toward a solution.",tone:"blue"},zoom:[1.03,1.12],pan:[20,-60],memory:true},
 {place:"street",title:"ON THE WAY HOME",caption:"It follows you long after you leave.",lead:{x:875,y:940,action:"walk",walk:1},zoom:[1.0,1.07],pan:[0,-80],memory:true},
 {place:"bedroom",title:"LATE AT NIGHT",caption:"Hours later, it comes back.",lead:{x:775,y:940,action:"sit"},zoom:[1.0,1.045],pan:[0,-35]},
 {place:"bedroom",title:"THE LOOP",caption:"You replay what you should have said.",lead:{x:765,y:940,action:"think"},sticker:{type:"compare",left:{label:"WHAT HAPPENED",title:"One moment",text:"A brief event in real life."},right:{label:"WHAT THE MIND DOES",title:"Endless replay",text:"The same moment gets repeated."},tone:"coral"},zoom:[1.045,1.13],pan:[-25,-85],thought:true},
 {place:"bedroom-phone",title:"THE CHECK",caption:"Then you reach for your phone.",lead:{x:760,y:940,action:"reach"},zoom:[1.08,1.13],pan:[-35,-90],notify:true},
 {place:"bedroom-phone",title:"ONE MORE LOOK",caption:"You check the conversation again.",lead:{x:760,y:940,action:"phone"},zoom:[1.13,1.2],pan:[-70,-125],notify:true},
 {place:"bedroom-phone",title:"THE FEEDBACK LOOP",caption:"Your attention feeds the loop.",lead:{x:760,y:940,action:"think"},sticker:{type:"steps",label:"BREAK THE LOOP",title:"Try a small reset",items:["Name the thought","Separate fact from guess","Return to the next action"],tone:"mint"},zoom:[1.2,1.1],pan:[-105,-45],thought:true,notify:true},
 {place:"bedroom-phone",title:"THE REALIZATION",caption:"Replaying is not the same as learning.",lead:{x:760,y:940,action:"reach"},zoom:[1.1,1.04],pan:[-45,10],phoneDown:true},
 {place:"bedroom-dawn",title:"A DIFFERENT RESPONSE",caption:"Name the thought. Don't argue with it.",lead:{x:1080,y:940,action:"turn"},zoom:[1.04,1.0],pan:[40,0]},
 {place:"park",title:"BACK TO THE PRESENT",caption:"Take the lesson. Let the rest pass.",lead:{x:730,y:940,action:"walk",walk:1},sticker:{type:"quote",text:"A thought can be noticed without being followed.",source:"A practical reminder",tone:"gold"},zoom:[1.0,1.04],pan:[0,-30],birds:true},
 {place:"park",title:"KEEP MOVING",caption:"Bring your attention back to now.",lead:{x:1110,y:940,action:"walk",walk:1},zoom:[1.04,1.0],pan:[-30,0],birds:true},
 {place:"park",title:"WISE-LAB",caption:"You are more than one awkward moment.",lead:{x:1110,y:940,action:"idle"},zoom:[1.0,1.0],pan:[0,0],end:true}
];

const validatedShots = validateStoryShots(shots);

function CharacterPhoneInHand({x,y,frame}){
 return <Phone x={x} y={y} frame={frame} tilt={lerp(frame,0,119,-7,5)} screen/>
}

function Shot({shot,index}){
 const f=useCurrentFrame();
 const local = Math.max(0,Math.min(119,f));
 const z=lerp(local,0,119,shot.zoom[0],shot.zoom[1]);
 const pan=lerp(local,0,119,shot.pan[0],shot.pan[1]);
 const fade=interpolate(local,[0,7,112,119],[0,1,1,0],clamp);
 const camX=(W-W*z)/2+pan, camY=(H-H*z)/2+Math.sin(local*.035)*3;
 const lead=shot.lead;
 const friend=shot.friend;
 const leaveX=friend&&friend.leave?lerp(local,0,119,friend.x||1390,1900):friend?.x;
 const isBedroom=shot.place.startsWith("bedroom");
 return <AbsoluteFill style={{background:"#101821",opacity:fade}}>
   <svg viewBox={"0 0 "+W+" "+H} width="100%" height="100%" style={{position:"absolute"}}>
    <defs>
      <linearGradient id="filmVignette" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#081019" stopOpacity=".12"/><stop offset=".6" stopColor="#081019" stopOpacity="0"/><stop offset="1" stopColor="#081019" stopOpacity=".42"/></linearGradient>
      <radialGradient id="focusGlow"><stop stopColor="#f4d6a3" stopOpacity=".19"/><stop offset="1" stopColor="#f4d6a3" stopOpacity="0"/></radialGradient>
    </defs>
    <g transform={"translate("+camX+" "+camY+") scale("+z+")"}>
      {shot.place==="cafe"||shot.place==="cafe-alone" ? <CafeSet frame={local}/> :
       shot.place==="street" ? <StreetSet frame={local}/> :
       shot.place==="park" ? <ParkSet frame={local}/> :
       <BedroomSet frame={local} dawn={shot.place==="bedroom-dawn"}/>}
      {shot.place==="cafe" && <>
        <CharacterRig x={lead.x} y={lead.y} frame={local} action={lead.action} talk={lead.talk} kind={lead.characterId || "alex"} s={1.03}/>
        {friend && <CharacterRig x={leaveX} y={friend.y} frame={local} action={friend.action} talk={friend.talk} kind={friend.characterId || "maya"} s={.94} walkAmount={friend.walk||0}/>}
        <CafeForeground frame={local} alone={false}/>
      </>}
      {shot.place==="cafe-alone" && <>
        <CharacterRig x={lead.x} y={lead.y} frame={local} action={lead.action} kind={lead.characterId || "alex"} s={1.08}/>
        <CafeForeground frame={local} alone={true}/>
      </>}
      {shot.place==="street" && <>
        <CharacterRig x={lerp(local,0,119,lead.x-45,lead.x+55)} y={lead.y} frame={local} action={lead.action} kind={lead.characterId || "alex"} s={1.04} walkAmount={1}/>
        {shot.memory && <MemoryPanel x={1280} y={255} frame={local} opacity={interpolate(local,[0,20,100,119],[0,.82,.82,0],clamp)}/>}
      </>}
      {isBedroom && <>
        <CharacterRig x={lead.x} y={lead.y} frame={local} action={lead.action} kind={lead.characterId || "arjun"} s={1.08} talk={false}/>
        <DeskProps frame={local} phone={true} faceDown={!!shot.phoneDown}/>
        {shot.place==="bedroom-phone" && shot.notify && <NotificationStack frame={local}/>}
        {shot.thought && <ThoughtLoop frame={local}/>}
        {shot.place==="bedroom-phone" && shot.lead.action==="phone" && <CharacterPhoneInHand x={890} y={555} frame={local}/>}
      </>}
      {shot.place==="park" && <>
        <CharacterRig x={lead.x} y={lead.y} frame={local} action={lead.action} kind={lead.characterId || "arjun"} s={1.06} walkAmount={lead.action==="walk"?1:0}/>
        {shot.birds && <ParkBirds frame={local}/>}
      </>}
      {shot.bubble && <g opacity={interpolate(local,[14,26,90,110],[0,1,1,0],clamp)}>
        <path d="M990 240 Q990 210 1020 210 H1320 Q1350 210 1350 240 V323 Q1350 353 1320 353 H1085 L1040 392 L1052 353 H1020 Q990 353 990 323Z" fill="#eee8dc"/>
        <text x="1170" y="270" fontSize="29" fill="#273542" fontFamily="Georgia" textAnchor="middle" fontStyle="italic">"So... anyway."</text>
      </g>}
    </g>
    <rect width={W} height={H} fill="url(#filmVignette)"/>
    <ellipse cx="980" cy="475" rx="900" ry="540" fill="url(#focusGlow)" opacity=".5"/>
   </svg>
   <StoryStickerLayer spec={shot.sticker}/>
   <div style={{position:"absolute",top:61,left:88,fontFamily:"Arial,sans-serif",fontWeight:700,fontSize:20,letterSpacing:5,color:"#e7c18e"}}>WISE-LAB <span style={{color:"#aab7bd",fontWeight:400,letterSpacing:3}}> / {shot.title}</span></div>
   <div style={{position:"absolute",left:0,right:0,bottom:0,height:202,background:"linear-gradient(180deg,rgba(10,17,25,0),rgba(10,17,25,.72))"}}/>
   <div style={{position:"absolute",left:230,right:230,bottom:68,textAlign:"center",fontFamily:"Arial,sans-serif",fontSize:36,fontWeight:700,lineHeight:1.2,color:"#fff7e9",letterSpacing:.15,textShadow:"0 3px 12px rgba(0,0,0,.75)"}}>{shot.caption}</div>
   <div style={{position:"absolute",left:88,right:88,top:28,height:2,background:"rgba(237,224,202,.24)"}}/>
   <div style={{position:"absolute",left:88,top:28,width:lerp(local,0,119,4,99)+"%",height:2,background:"#e7ba79"}}/>
   {shot.end && <div style={{position:"absolute",right:100,bottom:28,fontFamily:"Arial,sans-serif",fontSize:18,letterSpacing:6,color:"#f4e9d7",opacity:.8}}>UNDERSTAND YOUR MIND</div>}
 </AbsoluteFill>;
}

export const WiseLabFilm = () => <AbsoluteFill style={{background:"#101821"}}>
  {validatedShots.map((shot,i)=><Sequence key={i} from={i*120} durationInFrames={120}><Shot shot={shot} index={i}/></Sequence>)}
  <Sequence from={0} durationInFrames={1800}>
    <Audio src={staticFile("narration.mp3")} volume={.96}/>
    <Audio src={staticFile("ambience.wav")} volume={.2}/>
  </Sequence>
</AbsoluteFill>;
