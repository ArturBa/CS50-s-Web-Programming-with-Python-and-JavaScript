if (localStorage.getItem('username')) {
    let chat_id = localStorage.getItem('chat');
    location.replace(`/chat/${chat_id}`);
}

document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        // Button should emit a "add user" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const username = document.querySelector('#username').value;
                if (username.length < 5) {
                    alert('Username minimum length is 5 char');
                    return false;
                }
                socket.emit('add user', {'username': username});
                return false;
            };
        });
    });

    socket.on("user created", data => {
        localStorage.setItem('username', data.username);
        localStorage.setItem('chat', 'global');
        location.replace('/chat/global');
    });

});
