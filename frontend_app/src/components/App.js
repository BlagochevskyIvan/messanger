import React, {Component} from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import {render} from "react-dom";
import Chat from "./Chat";
import ChatDetail from "./ChatDetail";
import MainPage from "./MainPage";


export default class App extends Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <BrowserRouter>
                <Routes>
                    <Route path='/' exact element={<MainPage />} />
                    <Route path='/chat' exact element={<Chat />} />
                </Routes>
            </BrowserRouter>
            
        )
    }
}

const appDiv = document.getElementById('app');
render(<App/>, appDiv);