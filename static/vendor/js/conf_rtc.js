let user_id = document.getElementById("user_id").value

let config = {
    iceServers: [
        {urls: 'stun:178.250.157.153:3478'},
        {
            urls: "turn:178.250.157.153:3478",
            username: user_id,
            credential: "test123"
        }
    ],
    // iceTransportPolicy: "all"
};


// console.log(config)
let conn;
let peerConnection;
let dataChannel;
let btnCamera = document.querySelector('#getMedia')

const camera = document.querySelector('#myVideo');

const constraints = {
    video: true,
    audio: false
};

let localStream = new MediaStream()

function my_stream(e) {
    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            localStream = stream
            camera.srcObject = localStream
            camera.muted = true

            let audioTrack = stream.getAudioTracks()
            let videoTrack = stream.getVideoTracks()
            // audioTrack[0].enabled = false
            videoTrack[0].enabled = true

            console.log('stream', stream)
        }).catch(error => {
        console.log('Error media', error)
    })
}
// (event) => {}
// function foo(event){}
function connect() {
    const url = new URL(window.location)
    console.log(url.pathname) 
    conn = new WebSocket('ws://127.0.0.1:8000/ws' + url.pathname + '/')
    conn.addEventListener('open', (event) => {
        console.log("Connected to the signaling server");
        console.log(event);
        initialize(user_id);
    })
    
    conn.onmessage = function(event) {
        const data = JSON.parse(event.data);
        document.querySelector('#chat-log').value += (data.message + '\n');
        console.log("сообщение получено")
        console.log(event)
    };

    conn.onclose = function(event) {
        console.error('Chat socket closed unexpectedly');
    };

    let shiftIsPressed = false;

    $(window).keydown(function(event){
        if (event.keyCode == 16) {
            shiftIsPressed = true; 
            event.preventDefault();
        }
    }); 

    $(window).keyup(function(event){
        if (event.keyCode == 16) {
            shiftIsPressed = false;
            event.preventDefault();
        }    
    });

    $(window).on('keydown', function(event) {
    if (!shiftIsPressed && event.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
        }
    });


    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        conn.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
}

function send_message(){
    conn.send(JSON.stringify({'message':'HEllo'}))
    // dataChannel.send('hello')

}

function initialize(user_id) {
    peerConnection = new RTCPeerConnection(config)
    console.log(peerConnection)

    
    peerConnection.onicecandidate = function (event) {
        if (event.candidate) {
            send({
                peer: user_id,
                event: "candidate",
                data: event.candidate
            });
            console.log('event.candidate', event.candidate)
        }
    };

    dataChannel = peerConnection.createDataChannel("dataChannel", {
        reliable: true
    })

    dataChannel.onerror = function (error) {
        console.log("Error occured on datachannel:", error)
    }

    dataChannel.onmessage = function (event) {
        console.log("message:", event.data)
        chatLog.value += (event.data + '\n')
    }

    dataChannel.onclose = function () {
        console.log("data channel is closed")
        alert("Your interlocutor has disconnected")
    }

    peerConnection.ondatachannel = function (event) {
        dataChannel = event.channel
    }
    peerConnection.oniceconnectionstatechange = function(event){
        console.log("ICE",event)
    }
}

btnCamera.addEventListener('click', my_stream)

// document.addEventListener('DOMContentLoaded', connect)

let buttonConnect = document.querySelector("#btnConnect")
buttonConnect.addEventListener('click', connect)

let buttonSend = document.querySelector("#btnSend")
buttonSend.addEventListener('click', send_message)