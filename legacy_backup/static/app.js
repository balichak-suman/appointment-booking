let phoneNumber = '';
let userName = '';

function startChat() {
    phoneNumber = document.getElementById('phoneNumber').value;
    userName = document.getElementById('userName').value;

    if (!phoneNumber || !userName) {
        alert('Please enter both phone number and name');
        return;
    }

    document.getElementById('displayName').textContent = userName;
    document.getElementById('displayPhone').textContent = phoneNumber;

    document.getElementById('setupPanel').style.display = 'none';
    document.getElementById('chatContainer').style.display = 'flex';

    document.getElementById('messageInput').focus();
}

function resetChat() {
    document.getElementById('setupPanel').style.display = 'block';
    document.getElementById('chatContainer').style.display = 'none';

    // Clear messages except welcome message
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                <p>👋 Hi! I'm your hospital appointment assistant. How can I help you today?</p>
                <div class="timestamp">Just now</div>
            </div>
        </div>
    `;
}

function addMessage(text, isUser) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
            <div class="timestamp">${timeStr}</div>
        </div>
    `;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, true);
    input.value = '';

    try {
        // Send to webhook
        const response = await fetch('/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: {
                    text: message,
                    from: phoneNumber,
                    senderName: userName
                }
            })
        });

        const data = await response.json();

        // Add bot response to chat
        if (data.response) {
            setTimeout(() => {
                addMessage(data.response, false);
            }, 500);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('❌ Error: Could not send message. Is the server running?', false);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
