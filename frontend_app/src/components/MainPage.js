import React, {Component, useState} from "react";
import { useEffect } from "react";
import { Link, useNavigate, Outlet} from "react-router-dom";
import {Input, Button} from '@mui/material'

const MainPage = (props) => {
    const navigate = useNavigate();

    return(
        <div>
            <p>Введите логин</p>
            <Input > </Input>
            <Button variant="contained" onClick={() => navigate('/chat', {replace: false})}>nfjdfnjd</Button>
            
            
        </div>
        
    )
   
}

export default MainPage;