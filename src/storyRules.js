import {WISE_LAB_CAST, CAST_RULES} from "./wiseLabCast";

const STICKER_TYPES = new Set(["tag","stat","definition","steps","quote","compare"]);
const knownCast = new Set(Object.keys(WISE_LAB_CAST));

export function validateStoryShots(shots) {
  if (!Array.isArray(shots) || shots.length === 0) {
    throw new Error("A WISE-LAB episode must contain at least one story scene.");
  }
  for (const [index, shot] of shots.entries()) {
    const ids = [];
    if (shot.lead) ids.push(shot.lead.characterId || "arjun");
    if (shot.friend) ids.push(shot.friend.characterId || "maya");
    if (Array.isArray(shot.characters)) ids.push(...shot.characters.map(c => c.characterId || c.id));
    const unique = [...new Set(ids.filter(Boolean))];
    if (unique.length > CAST_RULES.maxSpeakingCharactersPerScene) {
      throw new Error("Scene "+index+" exceeds the small-cast limit of "+CAST_RULES.maxSpeakingCharactersPerScene+".");
    }
    for (const id of unique) {
      if (!knownCast.has(id)) {
        throw new Error("Scene "+index+" uses unknown character '"+id+"'. Add them to src/wiseLabCast.js only if they are a recurring cast member.");
      }
    }
    if (shot.sticker && !STICKER_TYPES.has(shot.sticker.type)) {
      throw new Error("Scene "+index+" uses unsupported sticker type '"+shot.sticker.type+"'.");
    }
  }
  return shots;
}

export const WISE_LAB_STORY_RULES = Object.freeze({
  castSize: Object.keys(WISE_LAB_CAST).length,
  maxCharactersPerScene: CAST_RULES.maxSpeakingCharactersPerScene,
  stickerTypes: [...STICKER_TYPES],
  principle: "Characters perform the story; stickers and typography explain the psychology.",
});
