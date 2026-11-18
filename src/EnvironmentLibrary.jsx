import React from "react";
const W=1920,H=1080;
const skyline=(night=false)=><g>
 <rect width="600" height="470" fill={night?"#1a2b40":"#a8c1c1"}/>
 <circle cx="480" cy="90" r="48" fill={night?"#e4d8ba":"#f0d09a"}/>
 {[0,1,2,3,4,5].map(i=><g key={i}><rect x={i*100} y={190+(i%3)*35} width="84" height={280-(i%3)*25} fill={night?"#30465a":"#778d91"}/>{[0,1,2].map(j=><rect key={j} x={i*100+15} y={215+(i%3)*35+j*62} width="20" height="25" fill={night?"#e5c58d":"#d6d3c1"} opacity=".65"/>)}</g>)}
</g>;

export function OfficeSet({frame=0}){return <g>
 <rect width={W} height={H} fill="#263642"/><rect y="0" width={W} height="760" fill="#47565b"/>
 <rect x="85" y="80" width="620" height="570" fill="#172b3d" stroke="#b18b63" strokeWidth="22"/><svg x="107" y="102" width="576" height="526" viewBox="0 0 600 470">{skyline(true)}</svg>
 <rect x="890" y="125" width="850" height="440" fill="#2b3a40"/>{[0,1,2,3,4].map(i=><g key={i}><rect x={935+i*155} y="170" width="112" height="340" fill="#634b3b"/><rect x={952+i*155} y="205" width="78" height="45" fill={["#8c9c9b","#c49a63","#607d87","#b47b62","#78917c"][i]}/></g>)}
 <path d="M0 760 H1920 V1080 H0Z" fill="#6a4c39"/>
 <rect x="260" y="715" width="1080" height="34" rx="8" fill="#8b684c"/><path d="M340 749 L320 1080 M1270 749 L1290 1080" stroke="#4d3c32" strokeWidth="30"/>
 <rect x="660" y="520" width="370" height="195" rx="12" fill="#17232e" stroke="#a5b3b4" strokeWidth="7"/><rect x="680" y="540" width="330" height="150" fill="#426778"/><path d="M845 715 V740 M785 740 H905" stroke="#a5b3b4" strokeWidth="12"/>
 <g transform="translate(1580 590)"><rect x="-60" y="0" width="120" height="180" fill="#604b3b"/><path d="M0 0 Q-115 -90 -78 -180 Q-10 -150 0 0 M0 0 Q105 -105 82 -180 Q15 -150 0 0" fill="#58765d"/></g>
</g>}

export function ClassroomSet({frame=0}){return <g>
 <rect width={W} height={H} fill="#34434a"/><rect y="0" width={W} height="760" fill="#d2c7ad"/>
 <rect x="120" y="95" width="550" height="470" fill="#172c3a" stroke="#8b7054" strokeWidth="22"/><svg x="142" y="117" width="506" height="426" viewBox="0 0 600 470">{skyline(false)}</svg>
 <rect x="830" y="95" width="920" height="460" rx="12" fill="#344e45" stroke="#6d604d" strokeWidth="20"/><path d="M910 210 Q1120 165 1320 215 M910 290 H1600 M910 370 Q1230 330 1540 370" stroke="#d6d8c8" strokeWidth="7" fill="none" opacity=".7"/>
 <path d="M0 760 H1920 V1080 H0Z" fill="#74563e"/>
 {[0,1,2,3].map(i=><g key={i} transform={"translate("+(120+i*445)+" "+(690+(i%2)*75)+")"}><path d="M0 0 H300 L325 38 H-20Z" fill="#b18a60"/><path d="M10 38 L0 270 M285 38 L300 270" stroke="#493b32" strokeWidth="20"/><rect x="85" y="-145" width="130" height="140" rx="10" fill="#34495a"/><path d="M105 -120 H195 M105 -90 H190" stroke="#d4d9d2" strokeWidth="5"/></g>)}
</g>}

export function LibrarySet({frame=0}){return <g>
 <rect width={W} height={H} fill="#27333b"/><rect y="0" width={W} height="790" fill="#51463d"/>
 {[0,1,2,3].map(i=><g key={i} transform={"translate("+(65+i*470)+" 85)"}><rect width="400" height="675" fill="#49382f" stroke="#a17b55" strokeWidth="18"/>
 {[0,1,2,3,4].map(row=><g key={row}><rect x="12" y={24+row*126} width="376" height="9" fill="#bd9a70"/>{[0,1,2,3,4,5,6,7,8].map(j=><rect key={j} x={20+j*40} y={36+row*126+(j%2)*5} width="30" height={82-(j%3)*8} rx="3" fill={["#8d5b48","#6e8290","#b18b56","#627764","#8a7184","#a96f55"][(j+i+row)%6]}/>)}</g>)}</g>)}
 <path d="M0 790 H1920 V1080 H0Z" fill="#6c4d38"/><rect x="390" y="710" width="1140" height="34" rx="10" fill="#9b7955"/><path d="M460 744 L440 1080 M1460 744 L1480 1080" stroke="#48372e" strokeWidth="28"/>
</g>}

export function LivingRoomSet({frame=0}){return <g>
 <rect width={W} height={H} fill="#283746"/><rect y="0" width={W} height="770" fill="#596064"/>
 <rect x="95" y="90" width="650" height="520" fill="#1d3040" stroke="#a17b5b" strokeWidth="24"/><svg x="119" y="114" width="602" height="472" viewBox="0 0 600 470">{skyline(false)}</svg>
 <rect y="770" width={W} height="310" fill="#684c3b"/>
 <rect x="520" y="600" width="950" height="250" rx="48" fill="#6d7b7b" stroke="#34434b" strokeWidth="18"/><rect x="570" y="550" width="850" height="190" rx="55" fill="#82918b"/>
 <rect x="660" y="620" width="210" height="115" rx="24" fill="#b77b62"/><rect x="1120" y="620" width="210" height="115" rx="24" fill="#9b8a72"/>
 <path d="M590 845 L570 1030 M1400 845 L1420 1030" stroke="#3e3430" strokeWidth="30"/>
 <rect x="1530" y="640" width="170" height="150" rx="10" fill="#4c3e35"/><path d="M1615 640 V430" stroke="#4c3e35" strokeWidth="16"/><path d="M1540 445 Q1615 365 1690 445 L1670 490 H1560Z" fill="#d2a56d"/>
</g>}
