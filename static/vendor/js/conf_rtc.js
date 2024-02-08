console.log(user_id)
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

function connect() {
    username = userInput.value
    if (username === '') {
        alert('Your name is empty!')
        return;
    }
    conn = new WebSocket('ws://127.0.0.1:8000/conf/' + 'test')
    conn.addEventListener('open', (e) => {
        console.log("Connected to the signaling server");
        initialize(username);
    })
    // conn.addEventListener('message', onmessage)

    btnCreateChat.style.display = 'block'
    connectButton.style.display = 'none'
    userInput.disabled = true
}

function initialize(username) {
    peerConnection = new RTCPeerConnection(config)

    peerConnection.onicecandidate = function (event) {
        if (event.candidate) {
            send({
                peer: username,
                event: "candidate",
                data: event.candidate
            });
            // console.log('event.candidate', event.candidate)
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