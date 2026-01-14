document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const modeSelector = document.getElementById('mode-selector');

    // Load saved mode
    chrome.storage.local.get(['mode'], function (result) {
        if (result.mode) {
            modeSelector.value = result.mode;
        }
    });

    modeSelector.addEventListener('change', () => {
        chrome.storage.local.set({ mode: modeSelector.value });
    });

    function appendMessage(text, type) {
        const div = document.createElement('div');
        div.classList.add('message', type);
        div.textContent = text;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        userInput.value = '';

        const mode = modeSelector.value;

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    mode: mode
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            appendMessage(data.response, 'system');

        } catch (error) {
            console.error('Error:', error);
            appendMessage('Error: Could not connect to SAM backend.', 'system');
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
