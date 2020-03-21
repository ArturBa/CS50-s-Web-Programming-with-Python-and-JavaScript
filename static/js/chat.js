if (localStorage.getItem('chat')) {
    console.log(location.href.substr(location.href.lastIndexOf('/') + 1));
}
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('chat-body').scrollBy(0, document.getElementById('chat-body').clientHeight);
    document.getElementById('chat-head').innerHTML = `:${localStorage.getItem('chat')}`;
    document.querySelector('title').innerHTML = `:${localStorage.getItem('chat')}`;
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // By default, submit button is disabled
    document.getElementById('new-msg-submit').disabled = true;

    // Enable button only if there is text in the input field
    document.getElementById('new-msg').onkeyup = () => {
        document.getElementById('new-msg-submit').disabled = document.getElementById('new-msg').value.length <= 0;
    };

    document.querySelector('#chat-form').onsubmit = () => {
        socket.emit('add msg', {
            'msg': document.querySelector('#new-msg').value,
            'chat_id': localStorage.getItem('chat'),
            'user_id': localStorage.getItem('username')
        });
        document.querySelector('#new-msg').value = '';
        document.querySelector('#new-msg-submit').disabled = true;
        return false;
    };

    socket.on("new msg", data => {
        if (data.chat_id !== localStorage.getItem('chat'))
            return false;
        const li = document.createElement('li');
        li.innerHTML = `<p class="msg-user">${localStorage.getItem('username')}</p> ` +
            `<p class="msg-time">${data.timestamp}</p>` +
            `<p class="msg-text">${data.msg}</p>`;
        document.querySelector('#chat-msgs').append(li);

        let chat = document.getElementById('chat-body');
        let bottom = chat.clientHeight + chat.scrollTop >= chat.scrollHeight;
        if (bottom) {
            chat.scroll(0, chat.clientHeight);
        }
        return false;
    });

});

