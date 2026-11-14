import React from "react";
import {Composition} from "remotion";
import {WiseLabFilm} from "./WiseLabFilm";
export const Root = () => <Composition id="WiseLab" component={WiseLabFilm} durationInFrames={1800} fps={30} width={1920} height={1080} />;