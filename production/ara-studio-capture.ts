/** WISE-LAB's first real 3D story pilot, rendered by Ara Studio's real-time scene exporter. */
import { writeFileSync } from 'node:fs';
import { parseProject, presetCode, type StudioProject } from '../src/studio/project';
import { decodeCharacter, encodeCharacter } from '../src/app/share';
import { yearsToAge } from '../src/core/params';
import { defaultAudio } from '../src/studio/audio/schema';
interface Harness { enabled:boolean; step(name:string,fn:()=>Promise<void>):Promise<void>; evaluate<T=unknown>(source:string):Promise<T>; ready():Promise<void>; pause(ms?:number):Promise<unknown>; folder:string }
function mainCharacter():string {
 const base=decodeCharacter(presetCode('Athletic man'),'medium');
 if(!base)throw new Error('Could not load WISE-LAB lead preset.');
 return encodeCharacter({...base,name:'WISE-LAB Main',seed:241114,gender:1,age:yearsToAge(22),muscle:.58,weight:.48,height:.56,african:.30,asian:.28,caucasian:.42,eyes:'brownlight',hair:'short02',hairColor:'#171719',hairTint:'#171719',facialHair:'none',outfit:'none',top:'tattered_shirt',jacket:'techwear_jacket',bottom:'techwear_pants',shoes:'shoes01',hat:'none',carry:'phone',expression:'neutral',garmentStyles:{tattered_shirt:{pattern:'solid',color:'#252c36',color2:'#151b25'},techwear_jacket:{pattern:'solid',color:'#292f3b',color2:'#465365'},techwear_pants:{pattern:'solid',color:'#151a23',color2:'#303744'}}});
}
function partnerCharacter():string {
 const base=decodeCharacter(presetCode('The Female Executive'),'medium');
 if(!base)throw new Error('Could not load second character preset.');
 return encodeCharacter({...base,name:'Maya',seed:241115,carry:'none',expression:'neutral'});
}
function buildPilot():StudioProject {
 const audio=defaultAudio();audio.muted=true;
 return parseProject(JSON.stringify({
  kind:'ara-studio',version:2,title:'WISE-LAB — The Loop',template:'street-cafe',camera:'dolly',
  view:{azimuth:20,elevation:14,zoom:1},aspect:'landscape',caption:false,
  actors:[
   {id:'lead',character:mainCharacter(),detail:'high',x:-3.4,y:0,z:-3.03,yaw:0,beats:[
    {id:'l1',clip:'sit_idle',duration:1.5,move:false},{id:'l2',clip:'stand_up',duration:1,move:false},
    {id:'l3',clip:'talk_gestures',duration:3,move:false},{id:'l4',clip:'sit_down',duration:1,move:false},
    {id:'l5',clip:'sit_idle',duration:2,move:false},{id:'l6',clip:'texting',duration:6.5,move:false}]},
   {id:'friend',character:partnerCharacter(),detail:'high',x:-3.4,y:0,z:-1.47,yaw:180,beats:[
    {id:'f1',clip:'sit_idle',duration:1.5,move:false},{id:'f2',clip:'stand_up',duration:1,move:false},
    {id:'f3',clip:'talk_gestures',duration:3.3,move:false},{id:'f4',clip:'idle',duration:.5,move:false},
    {id:'f5',clip:'walk',duration:8.7,move:true}]}
  ],
  shots:[
   {id:'s1',duration:3,shot:'wide',target:'all',view:{azimuth:20,elevation:14,zoom:1},camera:'dolly'},
   {id:'s2',duration:3,shot:'medium',target:'lead',view:{azimuth:10,elevation:5,zoom:1.1},camera:'locked'},
   {id:'s3',duration:4,shot:'wide',target:'friend',view:{azimuth:55,elevation:10,zoom:1.1},camera:'dolly'},
   {id:'s4',duration:5,shot:'medium',target:'lead',view:{azimuth:-25,elevation:7,zoom:1.2},camera:'dolly'}
  ],
  texts:[
   {id:'brand',text:'WISE-LAB',start:.25,duration:2.2,style:'text',anchor:'screen',x:.5,y:.12,size:30,color:'#ffffff'},
   {id:'thought',text:'THE MOMENT IS OVER',start:10.6,duration:2.6,style:'text',anchor:'screen',x:.5,y:.14,size:38,color:'#ffffff'}
  ],audio
 }));
}
export async function captureStudioExample(h:Harness) {
 if(!h.enabled)return;
 const{step,evaluate:e,ready,pause,folder}=h;
 await step('Example WISE-LAB 3D pilot renders two rigged characters and a continuous story',async()=>{
  await ready();const project=buildPilot();
  const times=[project.actors[0].beats.reduce((s,b)=>s+b.duration,0),project.actors[1].beats.reduce((s,b)=>s+b.duration,0),project.shots.reduce((s,b)=>s+b.duration,0)];
  if(times.some(v=>Math.abs(v-15)>.01))throw new Error('Action and camera tracks must run exactly 15 seconds.');
  await e('(async()=>{await studio.setProject('+JSON.stringify(project)+';)})()'.replace('+;','')));
  await ready();await pause(500);
  const info=await e<{actors:number;duration:number;clips:string[]}>('(()=>({actors:studio.project.actors.length,duration:Math.max(...studio.project.actors.map(a=>a.beats.reduce((s,b)=>s+b.duration,0)),studio.project.shots.reduce((s,b)=>s+b.duration,0)),clips:studio.project.actors.flatMap(a=>a.beats.map(b=>b.clip))}))()');
  if(info.actors!==2||info.duration<14.99||!info.clips.includes('texting')||!info.clips.includes('walk'))throw new Error('WISE-LAB story project failed validation: '+JSON.stringify(info));
  const size=await e<{width:number;height:number}>('(async()=>await studio.supportsMp4(1920,1080)?{width:1920,height:1080}:{width:1280,height:720})()');
  await e('(()=>{window.__wiseLab3dRender={done:0,total:450,ready:false,error:""};const p=structuredClone(studio.project);studio.exportMovie(studio.scene,p,{width:'+size.width+',height:'+size.height+',signal:new AbortController().signal,progress:(done,total)=>Object.assign(window.__wiseLab3dRender,{done,total})}).then(blob=>{window.__wiseLab3dMovie=blob;window.__wiseLab3dRender.ready=true;},error=>{window.__wiseLab3dRender.error=String(error?.stack||error);});})()');
  const deadline=Date.now()+18*60*1000;let last=0;
  for(;;){const state=await e<{done:number;total:number;ready:boolean;error:string}>('window.__wiseLab3dRender');if(state.error)throw new Error('Ara Studio MP4 export failed: '+state.error);if(state.ready)break;if(Date.now()>deadline)throw new Error('15-second WISE-LAB render timed out.');if(state.done-last>=45){last=state.done;console.log('WISE-LAB 3D pilot: '+state.done+'/'+state.total+' frames');}await pause(800);}
  const data=await e<string>('new Promise(resolve=>{const r=new FileReader();r.onload=()=>resolve(String(r.result));r.readAsDataURL(window.__wiseLab3dMovie);})');
  const bytes=Buffer.from(data.split(',')[1],'base64');if(bytes.length<150000)throw new Error('MP4 export unexpectedly small: '+bytes.length+' bytes.');
  writeFileSync(folder+'/wise-lab-3d-pilot-silent.mp4',bytes);
  writeFileSync(folder+'/wise-lab-3d-pilot-render.json',JSON.stringify({renderer:'Ara Studio / Three.js / Mediabunny',width:size.width,height:size.height,fps:30,durationSeconds:15,actorCount:2,animationClips:info.clips,cameraShots:project.shots.length,location:project.template,validation:'browser MP4 export completed; final mux and ffprobe validation follow'},null,2));
  console.log('Saved WISE-LAB silent 3D pilot ('+(bytes.length/1024/1024).toFixed(2)+' MiB, '+size.width+'x'+size.height+').');
 });
}
