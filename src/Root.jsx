import React from "react";
import {Composition} from "remotion";
import {WiseLabFilm} from "./WiseLabFilm";
import {CricketStory} from "./CricketStory";

export const Root = () => (
  <>
    <Composition
      id="WiseLab"
      component={WiseLabFilm}
      durationInFrames={1800}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="CricketStory"
      component={CricketStory}
      durationInFrames={900}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
