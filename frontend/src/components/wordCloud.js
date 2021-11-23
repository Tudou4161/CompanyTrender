import React, {useRef, useEffect} from "react";
import * as d3 from 'd3';
import cloud from "d3-cloud";

const width = 400;
const height = 400;

const WordCloud = (props) => {
    useEffect(() => {
        const data = props.labels;
      
        cloud()
            .size([width, height])
            .words(data.map(function(d) {
              return {text: d, size: 10 + Math.random() * 90, test: "haha"};
            }))
            .padding(5)
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", end)
            .start();
    }) 
    return (
        <div>
            <h1>워드클라우드 분석 결과</h1>
            <div id="word-cloud"></div>
      </div>
    );
}

export default WordCloud;