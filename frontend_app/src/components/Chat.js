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
    <Grid container direction="column" justifyContent="flex-start"  alignItems="flex-start" height="100vh">
      <Grid item bgcolor={"gray"} height="10vh">
        <Typography>Чаты</Typography>
      </Grid>
      <Grid container direction="row" justifyContent="flex-start"  alignItems="flex-start" height="90vh">
        <Grid container direction="column" justifyContent="flex-start"  alignItems="flex-start" height="90vh" width="30vh">
        </Grid>
        <Grid container direction="column" justifyContent="flex-start"  alignItems="flex-start" height="90vh" width="70vh">
        </Grid>
      </Grid>
    </Grid>
  );
};
export default Chat;
