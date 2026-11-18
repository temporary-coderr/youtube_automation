// Reusable visual asset catalogue. Renderers resolve only IDs requested by a scene.
export const WISE_LAB_ASSETS = Object.freeze({
  characters:["alex","maya","ethan","zoe","oliver","arthur"],
  environments:{
    cafe:{layers:["architecture","windows","lighting","furniture","foreground"],mood:"social / warm"},
    "cafe-alone":{extends:"cafe",layers:["architecture","windows","lighting","furniture","foreground"],mood:"quiet / reflective"},
    street:{layers:["sky","distant-buildings","street-furniture","ground","atmosphere"],mood:"transition / reflective"},
    bedroom:{layers:["window","room-architecture","bedroom-furniture","lighting","foreground"],mood:"private / introspective"},
    "bedroom-phone":{extends:"bedroom",layers:["phone","notifications","screen-glow"],mood:"digital distraction"},
    "bedroom-dawn":{extends:"bedroom",lighting:"dawn",mood:"resolution"},
    office:{layers:["windows","city-view","bookshelves","workstation","floor"],mood:"work / focus"},
    classroom:{layers:["windows","chalkboard","desks","floor"],mood:"learning / group"},
    library:{layers:["bookshelves","reading-tables","lighting","floor"],mood:"study / reflection"},
    "living-room":{layers:["window","sofa","side-table","lamp","floor"],mood:"home / relationships"},
    park:{layers:["sky","distant-trees","midground-trees","path","foreground"],mood:"open / restorative"}
  },
  props:{
    phone:{interaction:["pick-up","hold","look-at","put-down"],anchors:["right-hand","left-hand","desk"]},
    notebook:{interaction:["pick-up","open","write","close"],anchors:["right-hand","desk","lap"]},
    mug:{interaction:["pick-up","hold","put-down"],anchors:["right-hand","table"]},
    backpack:{interaction:["wear","remove","carry","put-down"],anchors:["back","floor"]},
    chair:{interaction:["sit","stand"],anchors:["floor"]},desk:{interaction:["place-object"],anchors:["environment"]},
    book:{interaction:["pick-up","open","read","close"],anchors:["right-hand","lap","desk"]},
    lamp:{interaction:["switch-on","switch-off","adjust"],anchors:["desk","floor"]}
  },
  stickers:["tag","stat","definition","steps","quote","compare","diagram","timeline","callout"],
  motionClips:["idle","gesture","walk","turn","reach","phone","think","sit"],
  cameraMoves:["locked","push-in","pull-back","tracking","pan-left","pan-right","over-shoulder","parallax"],
  transitions:["cut","cross-dissolve","match-move","whip-pan","foreground-wipe"]
});
export function resolveSceneAssets(scene) {
  return {
    characters:[...new Set((scene.characters||[]).map(c=>c.characterId||c.id))],
    environment:scene.place||scene.environment||"cafe", props:[...new Set(scene.props||[])],
    sticker:scene.sticker?.type||null, motion:[...new Set((scene.characters||[]).map(c=>c.action||"idle"))],
    camera:scene.camera?.move||"push-in"
  };
}
