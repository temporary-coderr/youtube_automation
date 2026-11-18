// WISE-LAB recurring cast bible. Keep identity stable across every episode.
export const WISE_LAB_CAST = {
  arjun: {
    id: "arjun", name: "Arjun", role: "main narrator / relatable lead",
    skin: "#b9785d", skinShade: "#925d4c", shirt: "#26384c",
    pants: "#182333", hair: "#15171d", silhouette: "messy-fringe",
  },
  maya: {
    id: "maya", name: "Maya", role: "friend / contrasting perspective",
    skin: "#d09a79", skinShade: "#a8755e", shirt: "#b77a43",
    pants: "#27364a", hair: "#211b1a", silhouette: "soft-wave",
  },
  kabir: {
    id: "kabir", name: "Kabir", role: "friend / challenger",
    skin: "#9b684f", skinShade: "#744a3b", shirt: "#47766f",
    pants: "#202b39", hair: "#17191f", silhouette: "short-curl",
  },
  zoya: {
    id: "zoya", name: "Zoya", role: "friend / grounded voice",
    skin: "#c58c6d", skinShade: "#95664f", shirt: "#8b668f",
    pants: "#303047", hair: "#28202a", silhouette: "curly-bob",
  },
};

export const CAST_RULES = Object.freeze({
  maxSpeakingCharactersPerScene: 3,
  preferredRecurringCastSize: 4,
  allowNewCharacterByDefault: false,
  newCharacterReason: "Only add a recurring character when the story genuinely needs a new relationship role.",
});
