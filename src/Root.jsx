import React from "react";
import {Composition} from "remotion";
import {WiseLabFilm} from "./WiseLabFilm";
import {PremiumShowcase} from "./PremiumShowcase";
export const Root = () => <>
  <Composition id="WiseLab" component={WiseLabFilm} durationInFrames={1800} fps={30} width={1920} height={1080} />
  <Composition id="WiseLabShowcase" component={PremiumShowcase} durationInFrames={360} fps={30} width={1920} height={1080} />
</>;