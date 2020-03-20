if (!localStorage.getItem('username')) {
    location.replace(`/`);
}

let sidebar = true;

function sidebar_change() {
    if (sidebar) {
        sidebar = false;
        document.getElementById("sidebar").style.display = "none";
    } else {
        sidebar = true;
        document.getElementById("sidebar").style.display = "block";
    }

}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('hello-user').innerHTML = `Hi ${localStorage.getItem('username')}`;
    document.getElementById('chat-head').innerHTML = `:${localStorage.getItem('chat')}`;

    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // By default, submit button is disabled
    document.getElementById('new-msg-submit').disabled = true;

    // Enable button only if there is text in the input field
    document.getElementById('new-msg').onkeyup = () => {
        document.getElementById('new-msg-submit').disabled = document.getElementById('new-msg').value.length <= 0;
    };

    document.querySelector('#new-msg-form').onsubmit = () => {
        socket.emit('add msg', {
            'msg': document.querySelector('#new-msg').value,
            'chat_id': localStorage.getItem('chat'),
            'user_id': localStorage.getItem('username')
        });
        console.log('data send');
        document.querySelector('#new-msg').value = '';
        document.querySelector('#new-msg-submit').disabled = true;
        return false;
    };

    socket.on("new msg", data => {
        if (data.chat_id !== localStorage.getItem('chat'))
            return false;
        const li = document.createElement('li');
        li.innerHTML = `<p class="msg-user">${localStorage.getItem('username')}</p><p class="msg-text">${data.msg}</p>`;
        document.querySelector('#chat-msg').append(li);
        return false;
    });

});

