import React, {useRef, useEffect} from "react";
import Chart from "chart.js";

function Bar__(props) {

    const x_label = props.label;
    const query = props.query;
    let chart;
    
    var randomColorGenerator = function () { 
        return '#' + (Math.random().toString(16) + '0000000').slice(2, 8); 
    };

    const canvasDom = useRef(null);
    
    useEffect(() => {
        const ctx = canvasDom.current.getContext("2d");
        console.log(ctx);

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: x_label,
                datasets: [
                    {
                        label: "키워드",
                        data: props.count,
                        backgroundColor: randomColorGenerator()
                    },
                ]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }, []);

    const barClickFunc = (e) => {
        var pointIdx = chart.getElementAtEvent(e)[0]._index;
        window.open(`https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query=${query}+${x_label[pointIdx]}`);
    }

    return (
        <div>
            <h2>💈 키워드 빈도 수 막대그래프</h2>
            <canvas ref={canvasDom} 
            onClick={barClickFunc}
            style={{width: "1200px", height: "600px", textAlign: "center", marginLeft: "150px"}}></canvas>
        </div>
    );
}

export default Bar__;