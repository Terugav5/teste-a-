document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userMessage = userInput.value.trim();
        if (!userMessage) {
            return;
        }

        // Display user's message
        appendMessage(userMessage, 'sent');
        userInput.value = '';
        userInput.focus();

        // Show a thinking indicator
        const thinkingIndicator = appendMessage('...', 'received', true);

        try {
            // Send message to the backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Remove thinking indicator and display AI's response
            thinkingIndicator.remove();
            appendMessage(data.response, 'received');

        } catch (error) {
            console.error('Error fetching chat response:', error);
            thinkingIndicator.remove();
            appendMessage('Sorry, something went wrong. Please try again.', 'received error');
        }
    });

    function appendMessage(text, type, isThinking = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);

        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);

        if (isThinking) {
            p.classList.add('thinking');
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
        return messageDiv;
    }
});