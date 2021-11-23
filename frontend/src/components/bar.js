import React, {useRef, useEffect} from "react";
import Chart from "chart.js";

function Bar__(props) {

    const canvasDom = useRef(null);
    useEffect(() => {
        const ctx = canvasDom.current.getContext("2d");
        console.log(ctx);

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: props.label,
                datasets: [
                    {
                        label: "키워드",
                        data: props.count,
                    },
                ]
            },
            options: {
                responsive: false
            }
        });
    }, []);

    return (
        <div>
            <h2>💈 키워드 빈도 수 막대그래프</h2>
            <canvas ref={canvasDom} style={{width: "1200px", height: "600px", textAlign: "center", marginLeft: "150px"}}></canvas>
        </div>
    );
}

export default Bar__;