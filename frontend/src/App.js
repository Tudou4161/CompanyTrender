import React, {useState, useEffect} from "react";
import { useHistory } from "react-router";
import { Link, Route, Switch, Routes } from "react-router-dom"
import Contents from "./components/contents";
import SearchHeader from "./components/search-header";
import Spinner from "./components/spinner";

function App() {
  
  const [ isLoading, setIsLoading ] = useState(false);
  const [ key, setKey ] = useState(""); 

  const changeKey = (text) => {
    setKey(text);
  }

  const changeIsLoading = (Boolean) => {
    setIsLoading(Boolean);
  }

  return (
    <div className="App">
      <SearchHeader changeKey={changeKey} changeIsLoading={changeIsLoading} />
      {
        ( key === "" || key === undefined || key === null )? null : (
          isLoading === true ? <Spinner></Spinner> : <Contents query={key} changeIsLoading={changeIsLoading}/>
        )
      }
    </div>
  );
}

export default App;
