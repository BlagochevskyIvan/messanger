let user_id = document.getElementById("user_id").value

let config = {
    iceServers: [
        {urls: 'stun:178.250.157.153:3478'},
        {
            urls: "turn:178.250.157.153:3478",
            user_id: user_id
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
    conn = new WebSocket('ws://127.0.0.1:8000/ws/conf/' + 'test/')
    conn.addEventListener('open', (event) => {
        console.log("Connected to the signaling server");
        console.log(event);
        // initialize();
    })
    conn.addEventListener("message", (event) => {
        console.log("сообщение получено")
        console.log(event)
    })
    
    // conn.addEventListener('message', onmessage)
}

function send_message(){
    conn.send(JSON.stringify({'message':'HEllo'}))
}

function initialize() {
    peerConnection = new RTCPeerConnection(config)

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
}

btnCamera.addEventListener('click', my_stream)

// document.addEventListener('DOMContentLoaded', connect)

let buttonConnect = document.querySelector("#btnConnect")
buttonConnect.addEventListener('click', connect)

let buttonSend = document.querySelector("#btnSend")
buttonSend.addEventListener('click', send_message)