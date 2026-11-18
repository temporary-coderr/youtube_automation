// WISE-LAB recurring cast bible. Character identities are fixed reusable rigs.
export const WISE_LAB_CAST = Object.freeze({
  alex: {id:"alex", name:"Alex", role:"main relatable lead", ageBand:"young-adult", skin:"#b9785d", skinShade:"#925d4c", shirt:"#26384c", pants:"#182333", hair:"#15171d", silhouette:"messy-fringe", scale:1, ageStyle:"adult"},
  maya: {id:"maya", name:"Maya", role:"friend / contrasting perspective", ageBand:"young-adult", skin:"#d09a79", skinShade:"#a8755e", shirt:"#b77a43", pants:"#27364a", hair:"#211b1a", silhouette:"soft-wave", scale:0.98, ageStyle:"adult"},
  ethan: {id:"ethan", name:"Ethan", role:"friend / challenger", ageBand:"young-adult", skin:"#9b684f", skinShade:"#744a3b", shirt:"#47766f", pants:"#202b39", hair:"#17191f", silhouette:"short-curl", scale:1.01, ageStyle:"adult"},
  zoe: {id:"zoe", name:"Zoe", role:"friend / grounded perspective", ageBand:"young-adult", skin:"#c58c6d", skinShade:"#95664f", shirt:"#8b668f", pants:"#303047", hair:"#28202a", silhouette:"curly-bob", scale:0.98, ageStyle:"adult"},
  oliver: {id:"oliver", name:"Oliver", role:"child perspective", ageBand:"child", skin:"#c58b6b", skinShade:"#99674f", shirt:"#4c86a2", pants:"#34465c", hair:"#30251f", silhouette:"child-curly", scale:0.78, ageStyle:"child"},
  arthur: {id:"arthur", name:"Arthur", role:"elder perspective", ageBand:"elder", skin:"#c49a7e", skinShade:"#98735e", shirt:"#657b70", pants:"#39424b", hair:"#b8b9b2", silhouette:"silver-side-part", scale:0.98, ageStyle:"elder"},
});
export const CAST_RULES = Object.freeze({
  minCharactersPerVideo: 2, maxCharactersPerVideo: 7, maxCharactersPerScene: 2,
  preferredRecurringCastSize: 6, allowNewCharacterByDefault: false,
  newCharacterReason: "Only add a new recurring character when the supplied story genuinely needs a role the existing cast cannot fulfil. Design and rig the character before production.",
});
