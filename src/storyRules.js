import {WISE_LAB_CAST, CAST_RULES} from "./wiseLabCast";
const STICKER_TYPES = new Set(["tag","stat","definition","steps","quote","compare","diagram","timeline","callout"]);
const knownCast = new Set(Object.keys(WISE_LAB_CAST));
function characterIdsForShot(shot) {
  if (Array.isArray(shot.characters)) return shot.characters.map(c => c.characterId || c.id).filter(Boolean);
  return [shot.lead && (shot.lead.characterId || "alex"), shot.friend && (shot.friend.characterId || "maya")].filter(Boolean);
}
export function validateStoryShots(shots) {
  if (!Array.isArray(shots) || shots.length === 0) throw new Error("A WISE-LAB episode must contain at least one story scene.");
  const used = new Set();
  for (const [index, shot] of shots.entries()) {
    const ids = [...new Set(characterIdsForShot(shot))];
    if (ids.length > CAST_RULES.maxCharactersPerScene) throw new Error("Scene "+index+" exceeds the per-scene character limit of "+CAST_RULES.maxCharactersPerScene+".");
    for (const id of ids) {
      if (!knownCast.has(id)) throw new Error("Scene "+index+" uses unknown character '"+id+"'. Add a recurring rig to src/wiseLabCast.js first.");
      used.add(id);
    }
    if (shot.sticker && !STICKER_TYPES.has(shot.sticker.type)) throw new Error("Scene "+index+" uses unsupported sticker type '"+shot.sticker.type+"'.");
    if (shot.durationInFrames != null && (!Number.isInteger(shot.durationInFrames) || shot.durationInFrames < 45)) throw new Error("Scene "+index+" duration must be at least 45 frames.");
  }
  if (used.size < CAST_RULES.minCharactersPerVideo || used.size > CAST_RULES.maxCharactersPerVideo) throw new Error("A WISE-LAB video must use 2–7 distinct cast members; this plan uses "+used.size+".");
  return shots;
}
export const WISE_LAB_STORY_RULES = Object.freeze({
  minCharactersPerVideo: CAST_RULES.minCharactersPerVideo, maxCharactersPerVideo: CAST_RULES.maxCharactersPerVideo,
  maxCharactersPerScene: CAST_RULES.maxCharactersPerScene, stickerTypes: [...STICKER_TYPES],
  principle: "The user's script is immutable source material. AI directs visuals; it does not write or rewrite the story.",
});
