import {WISE_LAB_CAST} from "./wiseLabCast";
import {WISE_LAB_ASSETS} from "./wiseLabAssets";
import {validateStoryShots} from "./storyRules";
// AI may direct visual choices only. It cannot author, paraphrase or replace narration.
export function validateVisualDirection(plan) {
  if (!plan || !Array.isArray(plan.shots)) throw new Error("Visual direction must contain a shots array.");
  const ids=new Set();
  for (const [index,shot] of plan.shots.entries()) {
    const place=shot.place||shot.environment;
    if(place&&!WISE_LAB_ASSETS.environments[place]) throw new Error("Scene "+index+" requests unknown environment '"+place+"'.");
    const sceneCast = Array.isArray(shot.characters) ? shot.characters : [shot.lead,shot.friend].filter(Boolean);\n    for(const c of sceneCast) {
      const id=c.characterId||c.id;
      if(!WISE_LAB_CAST[id]) throw new Error("Scene "+index+" requests unknown fixed character '"+id+"'.");
      ids.add(id);
      if(c.action&&!WISE_LAB_ASSETS.motionClips.includes(c.action)) throw new Error("Scene "+index+" requests unsupported action '"+c.action+"'.");
    }
    for(const prop of shot.props||[]) if(!WISE_LAB_ASSETS.props[prop]) throw new Error("Scene "+index+" requests unknown prop '"+prop+"'.");
    if(shot.sticker&&!WISE_LAB_ASSETS.stickers.includes(shot.sticker.type)) throw new Error("Scene "+index+" requests unknown sticker '"+shot.sticker.type+"'.");
  }
  validateStoryShots(plan.shots);
  return {...plan,selectedCharacterIds:[...ids]};
}
