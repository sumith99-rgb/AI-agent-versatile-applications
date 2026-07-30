let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const talkButton = document.getElementById('talkButton');
const statusText = document.getElementById('statusText');
const pulseRing = document.querySelector('.pulse-ring');
const userTranscript = document.getElementById('userTranscript');
const aiTranscript = document.getElementById('aiTranscript');

let audioCtx;

async function initAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];
            await sendAudioToServer(audioBlob);
        };
    } catch (err) {
        console.error("Microphone access denied or failed", err);
        statusText.innerText = "Mic Error (Allow Permissions)";
        pulseRing.style.backgroundColor = "red";
        pulseRing.style.boxShadow = "0 0 10px red";
    }
}

async function sendAudioToServer(audioBlob) {
    statusText.innerText = "Processing...";
    pulseRing.style.backgroundColor = "#eab308";
    pulseRing.style.boxShadow = "0 0 10px #eab308";
    
    userTranscript.innerText = "Sending audio...";
    userTranscript.classList.add('visible');
    aiTranscript.classList.remove('visible');
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    
    try {
        const response = await fetch('/api/intercom', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === "success") {
            userTranscript.innerText = `You: "${data.user_text}"`;
            aiTranscript.innerText = `AI: "${data.ai_text}"`;
            aiTranscript.classList.add('visible');
            
            if (data.audio_url) {
                // We add a timestamp to prevent browser caching of the audio file
                const audio = new Audio(data.audio_url + "?t=" + new Date().getTime());
                statusText.innerText = "Speaking...";
                pulseRing.style.backgroundColor = "#3b82f6";
                pulseRing.style.boxShadow = "0 0 10px #3b82f6";
                
                audio.play();
                
                audio.onended = () => {
                    resetStatus();
                };
            } else {
                resetStatus();
            }
        } else {
            aiTranscript.innerText = "Error: " + data.message;
            aiTranscript.classList.add('visible');
            resetStatus();
        }
    } catch (err) {
        console.error(err);
        aiTranscript.innerText = "Network Error.";
        aiTranscript.classList.add('visible');
        resetStatus();
    }
}

function resetStatus() {
    statusText.innerText = "System Online";
    pulseRing.style.backgroundColor = "#10b981";
    pulseRing.style.boxShadow = "0 0 10px #10b981";
}

const startRecording = () => {
    if (!mediaRecorder) {
        initAudio();
        return; // The first click just asks for permission. User has to click again.
    }
    
    if (mediaRecorder.state === 'inactive') {
        isRecording = true;
        talkButton.classList.add('recording');
        document.querySelector('.button-text').innerText = 'Listening...';
        statusText.innerText = "Recording...";
        pulseRing.style.backgroundColor = "#ef4444";
        pulseRing.style.boxShadow = "0 0 10px #ef4444";
        audioChunks = [];
        mediaRecorder.start();
    }
};

const stopRecording = () => {
    if (isRecording && mediaRecorder.state === 'recording') {
        isRecording = false;
        talkButton.classList.remove('recording');
        document.querySelector('.button-text').innerText = 'Hold to Talk';
        mediaRecorder.stop();
    }
};

// Mouse events
talkButton.addEventListener('mousedown', startRecording);
window.addEventListener('mouseup', stopRecording);

// Touch events for mobile
talkButton.addEventListener('touchstart', (e) => {
    e.preventDefault();
    startRecording();
});
window.addEventListener('touchend', stopRecording);

// Initialize audio context to bypass autoplay restrictions
document.body.addEventListener('click', () => {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        initAudio();
    }
}, { once: true });
