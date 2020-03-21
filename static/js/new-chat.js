document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('chat-head').innerHTML = `:New chat`;

    document.getElementById('new-chat-user-id').value = localStorage.getItem('username');
    document.querySelector('form').onsubmit = () => {
        localStorage.setItem('chat', document.getElementById('new-chat-value').value);
    };
});
