import axios from "axios";
import { useState } from "react";
import Bar__ from "./bar";
import WordCloud from "./wordCloud";
import Links from "./links";
import Pie from "./pie";

const Contents = (props) => {

    const labels = props.label;
    const counts = props.count;
    const links = props.newsLink;
    const p_val = props.predictVal;
    const headers = props.newsHead;
    const query = props.query;

    return (
        <div className="charts">
            <Bar__ count={counts} label={labels} query={query}/>
            <br />
            <WordCloud label={labels}/>
            <br />
            <Pie p_val={p_val}/>
            <br />
            <Links link={links} header={headers}/>
            <br />
        </div>
    );
}

export default Contents;