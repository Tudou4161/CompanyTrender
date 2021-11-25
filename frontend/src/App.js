import React, {useState, useEffect} from "react";
import { useHistory } from "react-router";
import { Link, Route, Switch, Routes } from "react-router-dom"
import Contents from "./components/contents";
import SearchHeader from "./components/search-header";
import Spinner from "./components/spinner";
import axios from "axios";
import './App.css';

function App() {
  
  const [ isLoading, setIsLoading ] = useState(false);
  const [ key, setKey ] = useState(""); 
  const [ label, setLabel ] = useState([]);
  const [ count, setCount ] = useState([]);
  const [ newsLink, setNewLink ] = useState([]);
  const [ newsHead, setNewsHead ] = useState([]);
  const [ predictVal, setPredictVal ] = useState([]);

  const changeKey = (text) => {
    setKey(text);
  }

  const changeIsLoading = (Boolean) => {
    setIsLoading(Boolean);
  }


  useEffect(async() => {
    if (isLoading === true) {
      await axios.get("/api/getResult", {params : {query : key}})
      .then((res) => {
        //insert data
        let result = res.data;
        setLabel([...result.words]);
        setCount([...result.counts]);
        setNewLink([...result.news_link]);
        setPredictVal([...result.percentage]);
        setNewsHead([...result.news_header]);
        //spinner close
        setIsLoading(false);
        return console.log(label);
      }).catch((e) => {
        return alert(e);
      })
    }
  }, [isLoading])

  return (
    <div className="App">
      <SearchHeader changeKey={changeKey} changeIsLoading={changeIsLoading} />
      {
        ( key === "" || key === undefined || key === null )? null : (
          isLoading === true ? <Spinner /> : <Contents label={label} 
                                                count={count} 
                                                newsLink={newsLink} 
                                                predictVal={predictVal} 
                                                newsHead={newsHead}
                                                query={key}/>
        )
      }
    </div>
  );
}

export default App;
