import React from "react";
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from "remotion";

const W = 1920;
const H = 1080;
const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"};

function CricketGround({frame}) {
  const cloudA = interpolate(frame, [0, 900], [-80, 90]);
  const cloudB = interpolate(frame, [0, 900], [80, -55]);
  return (
    <g>
      <defs>
        <linearGradient id="storybook-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#8dc9e8"/>
          <stop offset="72%" stopColor="#f5d8a0"/>
          <stop offset="100%" stopColor="#f9e8bf"/>
        </linearGradient>
        <linearGradient id="storybook-grass" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#91b96b"/>
          <stop offset="100%" stopColor="#477b4b"/>
        </linearGradient>
        <radialGradient id="storybook-sun">
          <stop offset="0%" stopColor="#fff7c9"/>
          <stop offset="100%" stopColor="#f5bd62"/>
        </radialGradient>
        <filter id="soft-shadow" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="12"/>
        </filter>
      </defs>
      <rect width={W} height={H} fill="url(#storybook-sky)"/>
      <circle cx="1510" cy="190" r="92" fill="url(#storybook-sun)"/>
      <circle cx="1510" cy="190" r="122" fill="#fff1b7" opacity=".2"/>
      <g transform={`translate(${cloudA} 0)`} fill="#fff9e9" opacity=".9">
        <ellipse cx="330" cy="205" rx="115" ry="35"/>
        <circle cx="270" cy="185" r="45"/><circle cx="330" cy="164" r="58"/><circle cx="390" cy="188" r="43"/>
      </g>
      <g transform={`translate(${cloudB} 0)`} fill="#fff9e9" opacity=".78">
        <ellipse cx="1110" cy="285" rx="105" ry="30"/>
        <circle cx="1050" cy="267" r="38"/><circle cx="1110" cy="246" r="50"/><circle cx="1170" cy="270" r="38"/>
      </g>
      <path d="M0 560 Q240 430 470 555 T930 530 T1420 545 T1920 500 L1920 900 L0 900Z" fill="#9bbd78"/>
      <path d="M0 660 Q330 560 690 665 T1330 640 T1920 610 L1920 930 L0 930Z" fill="#78a85e"/>
      <g fill="#4f8050">
        {Array.from({length:9}, (_, i) => (
          <g key={i} transform={`translate(${70 + i * 225} ${510 + (i % 3) * 32})`}>
            <rect x="-12" y="0" width="24" height="150" rx="10" fill="#8b6547"/>
            <circle cx="0" cy="-35" r="58" fill={i % 2 ? "#5e9259" : "#6c9d5d"}/>
            <circle cx="-34" cy="-10" r="38" fill="#78aa68"/>
            <circle cx="32" cy="-8" r="40" fill="#4f8552"/>
          </g>
        ))}
      </g>
      <path d="M0 775 Q500 715 960 770 T1920 745 L1920 1080 L0 1080Z" fill="url(#storybook-grass)"/>
      <path d="M0 850 Q480 805 960 850 T1920 830" fill="none" stroke="#b8cf83" strokeWidth="8" opacity=".35"/>
      <path d="M700 900 Q960 820 1220 900 L1220 1080 L700 1080Z" fill="#c9a77b" opacity=".7"/>
      <path d="M735 900 Q960 845 1185 900" fill="none" stroke="#ead0a2" strokeWidth="7" opacity=".8"/>
      <g fill="#f9e8bc" opacity=".65">
        {Array.from({length:38}, (_, i) => <circle key={i} cx={(i * 173 + 43) % W} cy={790 + (i * 47) % 260} r={2 + (i % 3)} />)}
      </g>
    </g>
  );
}

function Boy({x, y, scale=1, shirt="#e76f51", shorts="#365c83", catching=false, celebrating=false, frame=0}) {
  const armLift = catching
    ? interpolate(frame, [630, 700, 760], [0, 1, 1], clamp)
    : celebrating
      ? interpolate(frame, [790, 850, 900], [0, 1, 1], clamp)
      : 0;
  const leftArm = catching || celebrating
    ? `M-53 -130 Q-112 -${150 + armLift * 70} -${105 + armLift * 10} -${205 + armLift * 65}`
    : "M-53 -130 Q-115 -80 -105 -15";
  const rightArm = catching || celebrating
    ? `M53 -130 Q112 -${150 + armLift * 70} ${105 + armLift * 10} -${205 + armLift * 65}`
    : "M53 -130 Q115 -80 105 -15";
  const bounce = celebrating ? Math.sin(frame * .23) * 10 : 0;
  return (
    <g transform={`translate(${x} ${y + bounce}) scale(${scale})`}>
      <ellipse cx="0" cy="8" rx="104" ry="19" fill="#274b36" opacity=".25" filter="url(#soft-shadow)"/>
      <path d="M-52 -10 L-43 105 L-9 105 L0 35 L12 105 L48 105 L55 -10Z" fill={shorts}/>
      <path d="M-39 92 L-52 190 Q-23 204 -4 190 L8 105 L22 190 Q48 204 66 188 L47 92Z" fill="#f0c18b"/>
      <path d="M-56 175 Q-25 164 -1 183 L-7 207 L-65 207Z" fill="#59463b"/>
      <path d="M18 183 Q42 164 67 177 L80 207 L18 207Z" fill="#59463b"/>
      <path d="M-68 -145 Q0 -177 68 -145 L79 -10 Q0 12 -79 -10Z" fill={shirt} stroke="#9a4c3e" strokeWidth="5"/>
      <path d={leftArm} fill="none" stroke="#b97853" strokeWidth="28" strokeLinecap="round"/>
      <path d={rightArm} fill="none" stroke="#b97853" strokeWidth="28" strokeLinecap="round"/>
      <circle cx={catching || celebrating ? -105 : -105} cy={catching || celebrating ? -205 - armLift * 65 : -15} r="17" fill="#b97853"/>
      <circle cx={105} cy={catching || celebrating ? -205 - armLift * 65 : -15} r="17" fill="#b97853"/>
      <path d="M-54 -212 Q-62 -302 0 -308 Q68 -302 57 -210 L45 -164 Q0 -130 -44 -165Z" fill="#c9855c" stroke="#8b573f" strokeWidth="4"/>
      <path d="M-60 -238 Q-75 -305 -15 -330 Q45 -344 70 -292 L58 -255 Q25 -281 -6 -268 Q-32 -254 -60 -238Z" fill="#342b29"/>
      <path d="M-49 -272 Q-22 -304 4 -293" stroke="#594039" strokeWidth="8" fill="none" strokeLinecap="round"/>
      <ellipse cx="-22" cy="-226" rx="7" ry="10" fill="#332b28"/>
      <ellipse cx="25" cy="-226" rx="7" ry="10" fill="#332b28"/>
      <path d={catching || celebrating ? "M-15 -190 Q0 -177 17 -190" : "M-14 -184 Q0 -177 14 -184"} stroke="#713d35" strokeWidth="5" fill="none" strokeLinecap="round"/>
      <path d="M-78 -143 Q-95 -60 -70 -20" stroke="#fff2d6" strokeWidth="7" opacity=".3" fill="none"/>
    </g>
  );
}

function Ball({frame}) {
  const xs = [0, 120, 240, 330, 420, 510, 600, 690, 780, 900];
  const x = interpolate(frame, xs, [530, 535, 590, 700, 825, 970, 1125, 1280, 1430, 1450], clamp);
  const y = interpolate(frame, xs, [560, 560, 525, 450, 360, 325, 370, 470, 585, 585], clamp);
  const scale = interpolate(frame, [0, 240, 330, 600, 690, 780, 900], [.85, .9, 1.45, 2.1, 1.5, .95, .9], clamp);
  const opacity = interpolate(frame, [0, 220, 240, 780, 810], [0, 0, 1, 1, 0], clamp);
  const spin = frame * 13;
  return (
    <g transform={`translate(${x} ${y}) scale(${scale}) rotate(${spin})`} opacity={opacity}>
      <circle r="23" fill="#fff1d2" stroke="#a94436" strokeWidth="5"/>
      <path d="M-10 -20 Q15 -5 10 20 M10 -20 Q-15 -5 -10 20" fill="none" stroke="#b84e40" strokeWidth="3.5" strokeLinecap="round"/>
      <path d="M-4 -19 Q1 -10 0 0" stroke="#fff" strokeWidth="3" opacity=".8"/>
    </g>
  );
}

function Bat({frame}) {
  const swing = interpolate(frame, [90, 145, 190, 240], [-48, 5, 76, 92], {extrapolateLeft:"clamp", extrapolateRight:"clamp", easing:Easing.inOut(Easing.quad)});
  const show = interpolate(frame, [75, 95, 230, 250], [0, 1, 1, 0], clamp);
  return (
    <g transform={`translate(470 610) rotate(${swing})`} opacity={show}>
      <rect x="-12" y="-180" width="24" height="82" rx="9" fill="#765039"/>
      <path d="M-12 -105 Q-42 -85 -48 -15 L-34 110 Q0 126 34 110 L48 -15 Q42 -85 12 -105Z" fill="#e7c58e" stroke="#9a754d" strokeWidth="6"/>
      <path d="M-27 -55 L-20 85" stroke="#fff0ca" strokeWidth="6" opacity=".5"/>
    </g>
  );
}

const storyBeats = [
  {at:0, title:"A PERFECT AFTERNOON", line:"Two friends. One bat. One bright red ball."},
  {at:120, title:"HERE COMES THE HIT!", line:"A mighty swing sends the ball soaring!"},
  {at:240, title:"AND THEN… TIME SLOWS DOWN", line:"The little red ball spins through the golden air."},
  {at:510, title:"EYES ON THE BALL!", line:"His friend takes a breath and reaches up…"},
  {at:690, title:"GOT IT!", line:"A wonderful catch! What a moment!"},
  {at:810, title:"BEST GAME EVER", line:"The two friends cheer beneath the sunny sky."}
];

function StoryCaption({frame}) {
  const beat = [...storyBeats].reverse().find(item => frame >= item.at) || storyBeats[0];
  const opacity = interpolate(frame % 30, [0, 5, 25, 30], [0, 1, 1, 0], clamp);
  return (
    <g opacity={opacity}>
      <rect x="310" y="920" width="1300" height="112" rx="34" fill="#fff4d9" stroke="#b98754" strokeWidth="6" opacity=".96"/>
      <text x="960" y="963" textAnchor="middle" fontFamily="Georgia, serif" fontSize="27" fontWeight="bold" letterSpacing="3" fill="#8d513b">{beat.title}</text>
      <text x="960" y="1008" textAnchor="middle" fontFamily="Georgia, serif" fontSize="31" fill="#493c32">{beat.line}</text>
    </g>
  );
}

export const CricketStory = () => {
  const frame = useCurrentFrame();
  const vignette = interpolate(frame, [0, 900], [.08, .16], clamp);
  const slowGlow = interpolate(frame, [230, 300, 650, 720], [0, .7, .7, 0], clamp);
  const celebration = frame >= 810;
  return (
    <AbsoluteFill style={{background:"#8dc9e8"}}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%">
        <CricketGround frame={frame}/>
        <path d="M0 0 H1920 V1080 H0Z" fill="#fff2d1" opacity={vignette * .12}/>
        <g opacity={interpolate(frame, [0, 240, 270], [1, 1, .35], clamp)}>
          <Boy x={470} y={700} scale={1.04} shirt="#e76f51" shorts="#365c83" frame={frame}/>
          <Bat frame={frame}/>
        </g>
        <Boy x={1450} y={700} scale={1.06} shirt="#4f91a5" shorts="#5a6486" catching={frame >= 630 && frame < 810} celebrating={celebration} frame={frame}/>
        <Ball frame={frame}/>
        <g opacity={slowGlow} pointerEvents="none">
          <circle cx="990" cy="390" r="270" fill="#fff4c7" opacity=".12"/>
          <path d="M610 180 Q960 70 1320 180" fill="none" stroke="#fff5cf" strokeWidth="5" strokeDasharray="10 24" opacity=".8"/>
          <text x="960" y="155" textAnchor="middle" fontFamily="Georgia,serif" fontSize="32" fontStyle="italic" fill="#fff8df" letterSpacing="7">S L O W   M O T I O N</text>
        </g>
        <g opacity={interpolate(frame, [210, 240, 690, 735], [0, .8, .8, 0], clamp)} fill="none" stroke="#fff6d9" strokeWidth="8" strokeLinecap="round">
          <path d="M650 545 Q850 420 1020 385" strokeDasharray="12 24"/>
          <path d="M680 585 Q860 490 1010 470" strokeDasharray="6 28" opacity=".6"/>
        </g>
        <StoryCaption frame={frame}/>
        <rect width={W} height={H} fill="#352a20" opacity={vignette} pointerEvents="none"/>
        <text x="84" y="82" fontFamily="Georgia,serif" fontSize="26" fontStyle="italic" fill="#fff4d9" opacity=".9">A LITTLE STORY OF FRIENDSHIP</text>
        <text x="1835" y="82" textAnchor="end" fontFamily="Georgia,serif" fontSize="23" fill="#fff4d9" opacity=".9">THE SLOW-MOTION SIX</text>
      </svg>
    </AbsoluteFill>
  );
};
