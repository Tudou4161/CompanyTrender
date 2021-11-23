import axios from "axios";
import { useState } from "react";

const SearchHeader = (props) => {

    const [ keyword, setKeyWord ] = useState("");

    const searchKeywordChange = (e) => {
        setKeyWord(e.target.value)
    }

    const searchClicked = () => {
        if (keyword === "" || keyword === undefined || keyword === null) {
            return alert("검색어를 다시 입력해주세요.");
        }
        props.changeKey(keyword);
        props.changeIsLoading(true);
    }

    return (
        <div className="search-header">
            <div className="title">
                <h1>📊Trender</h1>
            </div>
            <div className="search-bar">
                <input type="text" placeholder="검색어를 입력해주세요." onChange={searchKeywordChange} />
                <button onClick={searchClicked}>검색</button>
            </div>
        </div>
    );
}

export default SearchHeader;