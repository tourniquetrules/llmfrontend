document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const modelInput = document.getElementById('model-input');
    const tempInput = document.getElementById('temp-input');
    const tokensInput = document.getElementById('tokens-input');

    let history = [];

    function addMessage(text, sender, metrics = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const textDiv = document.createElement('div');
        textDiv.textContent = text;
        messageDiv.appendChild(textDiv);

        if (metrics) {
            const metricsDiv = document.createElement('div');
            metricsDiv.classList.add('metrics');
            metricsDiv.innerHTML = `
                <span>In: ${metrics.input_tokens}</span> |
                <span>Out: ${metrics.output_tokens}</span> |
                <span>Speed: ${metrics.tokens_per_second} t/s</span> |
                <span>Latency: ${metrics.total_time}s</span>
            `;
            messageDiv.appendChild(metricsDiv);
        }

        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        const model = modelInput.value.trim();
        const temperature = tempInput.value;
        const maxTokens = tokensInput.value;

        if (!text) return;

        addMessage(text, 'user');
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    model: model,
                    history: history,
                    temperature: temperature,
                    max_tokens: maxTokens
                })
            });

            const data = await response.json();

            if (response.ok) {
                addMessage(data.reply, 'bot', data.metrics);
                // Update history
                history.push({role: "user", content: text});
                history.push({role: "assistant", content: data.reply});
            } else {
                addMessage(`Error: ${data.error}`, 'error');
            }
        } catch (error) {
            addMessage(`Network Error: ${error.message}`, 'error');
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
