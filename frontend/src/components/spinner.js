import ScaleLoader from "react-spinners/ScaleLoader"

const Spinner = () => {
    return (
        <div style={{marginTop: "100px"}}>
            <ScaleLoader height="160" width="32" color="#6b5ce7" radius="8" />
            <h3>분석 리포트를 작성 중입니다...</h3>
        </div>
    )
}

export default Spinner;