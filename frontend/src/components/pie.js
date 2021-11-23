import React, {useRef, useEffect} from "react";
import Chart from "chart.js";

const Pie = (props) => {
    const canvasDom = useRef(null);
    useEffect(() => {
        const ctx = canvasDom.current.getContext("2d");
        console.log(ctx);

        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["부정", "중립", "긍정"],
                datasets: [
                    {
                        label: "키워드",
                        data: props.p_val,    
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)'
                          ],
                    },
                ],
            },
            options: {
                responsive: false
            }
        });
    }, []);

    return (
        <div>
            <h2>📄 뉴스 긍/부정도 분석 결과</h2>
            <canvas ref={canvasDom} width="600" height="600" style={{marginLeft: "400px"}}></canvas>
        </div>
    );
}

export default Pie;