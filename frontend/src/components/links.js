import React, {useRef, useEffect} from "react";
import Chart from "chart.js";

const Links = (props) => {
    return (
        <div className="news_box">
            <h2>🕓 최신 뉴스 링크</h2>
            {
                props.header.map((row, i) => (
                    <div className="news">
                        <h4>{props.header[i]}</h4>
                        <button><a href={props.link[i]}>링크로 이동</a></button>
                    </div>
                ))
            }
        </div>
    );
}

export default Links;