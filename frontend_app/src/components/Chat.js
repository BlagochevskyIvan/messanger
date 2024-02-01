import React, { Component, useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import { Input, Grid, Typography } from "@mui/material";

const Chat = (props) => {
  const base_url = "http://127.0.0.1:8000/chat/";

  const [messages, setMessages] = useState([[1]]);

  useEffect(() => {
    axios.get(base_url + "chat/").then((res) => {
      console.log(res.data);
      setMessages(res.data);
    });
  }, []);

  return (
    <Grid container direction="row" justifyContent="center" height="70vh">
      <Grid item bgcolor={"red"} xs={3}>
        <Grid item direction="column">
            <Typography>Чаты</Typography>
        </Grid>
      </Grid>
      <Grid item xs={7}>nfmdjk</Grid>
    </Grid>
  );
};
export default Chat;
