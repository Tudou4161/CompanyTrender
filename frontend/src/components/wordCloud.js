import React, {useRef, useEffect} from "react";
import * as d3 from 'd3';
import cloud from "d3-cloud";

const width = 800;
const height = 800;

const WordCloud = (props) => {

    var fill = function(i) {
        return d3.schemeCategory10[i];
    }

    useEffect(() => {
        const data = props.label;
      
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

        function end(words) {
            d3.select("#word-cloud")
                .append("svg")
                .attr("width", 800)
                .attr("height", 800)
                .style("border", "1px solid black")
                .append("g")
                .attr("transform", "translate(" + 800 / 2 + "," + 800 / 2 + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("font-family", "Impact")
                .style("fill", function (d, i) {
                    return fill(i);
                })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
            }
    }) 
    return (
        <div>
            <h2>☁️ 워드클라우드 분석 결과</h2>
            <div id="word-cloud"></div>
      </div>
    );
}

export default WordCloud;