import React from "react";
import {Composition} from "remotion";
import {WiseLabFilm} from "./WiseLabFilm";
import {GENERATED_SCENE_PLAN} from "./generatedScenePlan";
export const Root = () => <Composition id="WiseLab" component={WiseLabFilm} durationInFrames={GENERATED_SCENE_PLAN.durationInFrames || 1800} fps={30} width={1920} height={1080} />;
