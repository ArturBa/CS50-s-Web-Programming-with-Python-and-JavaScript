document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('chat-head').innerHTML = `:All chats`;

});

const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function add_user_chat(chat_id) {
    socket.emit('add user to chat', {
        'user_id': localStorage.getItem('username'),
        'chat_id': chat_id
    });
    return false;
}

socket.on('user added to chat', data => {
    localStorage.setItem('chat', data.chat_id);
    location.replace(`/chat/${data.chat_id}`);
});
