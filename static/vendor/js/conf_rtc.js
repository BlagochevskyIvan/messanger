let user_id = document.getElementById("user_id").value;

let config = {
    iceServers: [
        { urls: "stun:178.250.157.153:3478" },
        {
            urls: "turn:178.250.157.153:3478",
            username: user_id,
            credential: "test123",
        },
    ],
    // iceTransportPolicy: "all"
};

// console.log(config)
let conn;
let peerConnection;
let dataChannel;
let btnCamera = document.querySelector("#getMedia");

const camera = document.querySelector("#myVideo");

const constraints = {
    video: true,
    audio: false,
};

let localStream = new MediaStream();

function my_stream(e) {
    navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
        localStream = stream;
        camera.srcObject = localStream;
        camera.muted = true;
        
        let audioTrack = stream.getAudioTracks();
        let videoTrack = stream.getVideoTracks();
        // audioTrack[0].enabled = false
        videoTrack[0].enabled = true;
        
        console.log("stream", stream);
    })
    .catch((error) => {
        console.log("Error media", error);
    });
    createOffer()
}

// (event) => {}
// function foo(event){}

function send(message) {
    conn.send(JSON.stringify(message));
}

function createOffer(){
    if (localStream){
        console.log("добавлены", localStream);
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream)
        })
    }
    console.log('оффер')
    peerConnection.createOffer((offer) => {
        send({
            peer: user_id,
            event: "offer",
            type: "offer",
            data: offer
        })
        peerConnection.setLocalDescription(offer);
    }, (error) => {
        console.log('Ошибка в создании оффера', error)
    })
}

function handleOffer(data){
    console.log('offer', data)

}

function handleChatMessage(data){
    console.log('chat_message', data)
    document.querySelector("#chat-log").value += data.message + "\n";
    console.log("сообщение получено");
}
function handleICECandidate(data){
    console.log('iceCandidate', data)
}
function handleAnswer(){

}

function on_message(message){
    console.log('message',message)
    const content = JSON.parse(message.data)
    const data = content.data 
    console.log('content',content)
    console.log('data',data)

    // if (content.peer == user_id){
    //     return
    // }
    if (content.type == 'offer'){
        console.log('offer')
        handleOffer(content)
    }
    else if (content.type == 'chat_message'){
        handleChatMessage(content) 
    }
    else if (content.type == 'candidate'){
        console.log('iceCandidate')
        handleICECandidate(content)
    }
    
}


function initialize(user_id) {
    peerConnection = new RTCPeerConnection(config);
    console.log('peerConnection', peerConnection);

    peerConnection.onicecandidate = function (event) {
        if (event.candidate) {
            send({
                peer: user_id,
                type: "candidate",
                data: event.candidate,
            });
            console.log("event.candidate", event.candidate);
        }
    };

    dataChannel = peerConnection.createDataChannel("dataChannel", {
        reliable: true,
    });

    dataChannel.onerror = function (error) {
        console.log("Error occured on datachannel:", error);
    };

    dataChannel.onmessage = function (event) {
        console.log("message:", event.data);
        chatLog.value += event.data + "\n";
    };
    

    dataChannel.onclose = function () {
        console.log("data channel is closed");
        alert("Your interlocutor has disconnected");
    };

    peerConnection.ondatachannel = function (event) {
        dataChannel = event.channel;
    };
    peerConnection.oniceconnectionstatechange = function (event) {
        console.log("ICE", event);
    };
}



function connect() {
    const url = new URL(window.location);
    console.log(url.pathname);
    conn = new WebSocket("ws://127.0.0.1:8000/ws" + url.pathname + "/");

    conn.addEventListener("open", (event) => {
        console.log("Connected to the signaling server");
        console.log(event);
        conn.send(
            JSON.stringify({type: "login", data: { user_id: user_id } })
        );
        initialize(user_id);
    });

    conn.onmessage = function (message) {
        on_message(message)
    };

    conn.onclose = function (event) {
        console.error("Chat socket closed unexpectedly");
    };

    let shiftIsPressed = false;

    $(window).keydown(function (event) {
        if (event.keyCode == 16) {
            shiftIsPressed = true;
            event.preventDefault();
        }
    });

    $(window).keyup(function (event) {
        if (event.keyCode == 16) {
            shiftIsPressed = false;
            event.preventDefault();
        }
    });

    $(window).on("keydown", function (event) {
        if (!shiftIsPressed && event.keyCode === 13) {
            document.querySelector("#chat-message-submit").click();
        }
    });

    document.querySelector("#chat-message-submit").onclick = function (e) {
        const messageInputDom = document.querySelector("#chat-message-input");
        const message = messageInputDom.value;
        send({
            type: "chat_message",
            message: message,
        });

        messageInputDom.value = "";
    };
}


btnCamera.addEventListener("click", my_stream);

// document.addEventListener('DOMContentLoaded', connect)

let buttonConnect = document.querySelector("#btnConnect");
buttonConnect.addEventListener("click", connect);

let buttonSend = document.querySelector("#btnSend");
buttonSend.addEventListener("click", (event) => {
    send({
        type: "chat_message",
        "event": "chat_message",
        "message": "Hello",
    });
});
