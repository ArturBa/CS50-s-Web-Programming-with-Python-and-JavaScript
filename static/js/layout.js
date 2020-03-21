if (!localStorage.getItem('username')) {
    location.replace(`/`);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('hello-user').innerHTML = `Hi ${localStorage.getItem('username')}`;
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.emit('get chats', {'user_id': localStorage.getItem('username')});

    // Get chats from a user
    socket.on("user chats", data => {
        let chats = document.getElementById('chat-list');
        for (let chat in data.chats) {
            if (data.chats.hasOwnProperty(chat)) {
                const li = document.createElement('li');
                li.innerHTML = `<a href="/chat/${data.chats[chat]}">:${data.chats[chat]} </a>`;
                chats.append(li);
            }
        }
        return false;
    });

    // Set up color mode
    if (localStorage.getItem('dark-mode') === 'true') {
        document.querySelector('body').classList.add('dark-mode');
        document.getElementById('mode').checked = true;
    } else {
        document.getElementById('mode').checked = false;
    }

    // Add dark mode
    document.getElementById('mode').onchange = function () {
        if (this.checked === true) {
            document.querySelector('body').classList.add('dark-mode');
            localStorage.setItem('dark-mode', 'true');
        } else {
            document.querySelector('body').classList.remove('dark-mode');
            localStorage.setItem('dark-mode', 'false');
        }
    }
});

