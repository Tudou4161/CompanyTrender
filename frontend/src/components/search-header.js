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
        <div>
            <input type="text" placeholder="검색어를 입력해주세요." onChange={searchKeywordChange} />
            <button onClick={searchClicked}>검색</button>
        </div>
    );
}

export default SearchHeader;