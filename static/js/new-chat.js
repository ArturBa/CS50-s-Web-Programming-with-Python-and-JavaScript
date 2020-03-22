document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('new-chat-user-id').value = localStorage.getItem('username');
    const chat = document.getElementById('new-chat-value');
    const chatError = document.querySelector('span.error');
    document.querySelector('form').onsubmit = (event) => {
        // if the username field is valid, we let the form submit
        if (!chat.validity.valid) {
            event.preventDefault();
            // If it isn't, we display an appropriate error message
            showError();
        } else {
            localStorage.setItem('chat', document.getElementById('new-chat-value').value);
        }
    };

    function showError() {
        if (chat.validity.valueMissing) {
            // If the field is empty
            // display the following error message.
            chatError.textContent = 'You need to enter a chat name.';
        } else if (chat.validity.tooShort) {
            // If the data is too short
            // display the following error message.
            chatError.textContent = `Chat name should be at least ${chat.minLength} characters; you entered ${chat.value.length}.`;
        }

    }
});
