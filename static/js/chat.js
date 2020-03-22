if (localStorage.getItem('chat')) {
    localStorage.setItem('chat', (location.href.substr(location.href.lastIndexOf('/') + 1)));
}
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('chat-body').scroll(0, document.getElementById('chat-body').scrollHeight);
    document.getElementById('chat-name').innerHTML = `:${localStorage.getItem('chat')}`;
    document.querySelector('title').innerHTML = `:${localStorage.getItem('chat')}`;
    document.getElementById('leave-chat-user-id').value = localStorage.getItem('username');
    document.getElementById('leave-chat-chat-id').value = localStorage.getItem('chat');
    const message = document.getElementById('new-msg');
    const messageError = document.getElementById('new-msg-error');
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    socket.on('connect', () => {
        document.querySelector('#chat-form').onsubmit = function (event) {
            event.preventDefault();
            if (!message.validity.valid) {
                // If message invalid show error
                showError();
                return false;
            }
            socket.emit('add msg', {
                'msg': document.querySelector('#new-msg').value,
                'chat_id': localStorage.getItem('chat'),
                'user_id': localStorage.getItem('username')
            });
            document.querySelector('#new-msg').value = '';
            return false;
        };

        socket.on("new msg", data => {
            // Get new message
            if (data.chat_id !== localStorage.getItem('chat')) {
                // If it's not for this chat end
                return false;
            }
            if (data.user_id !== localStorage.getItem('username')) {
                // Play notification when someone else posted
                const audio = new Audio('/static/snd/hollow.mp3');
                audio.play();
            }
            // Create new message
            const li = document.createElement('li');
            li.innerHTML = `<p class="msg-user">${data.user_id}</p> ` +
                `<p class="msg-time">${data.timestamp}</p>` +
                `<div class="msg-text">${data.msg}</div>`;

            // Get current position on chat
            let chat = document.getElementById('chat-body');
            let bottom = chat.clientHeight + chat.scrollTop >= chat.scrollHeight;

            // Add message
            document.querySelector('#chat-msgs').append(li);
            // If user was on chat bottom autoscroll
            if (bottom) {
                chat.scroll(0, chat.scrollHeight);
            }
            return false;
        });
    });


    message.addEventListener('input', () => {
        // Each time the user types something, we check if the
        // form fields are valid.

        if (message.validity.valid) {
            // In case there is an error message visible, if the field
            // is valid, we remove the error message.
            messageError.innerHTML = ''; // Reset the content of the message
            messageError.className = 'error'; // Reset the visual state of the message
        }
    });

    function showError() {
        if (message.validity.valueMissing) {
            // If the field is empty
            // display the following error message.
            messageError.textContent = 'You need to enter a message.';
        } else if (message.validity.tooShort) {
            // If the data is too short
            // display the following error message.
            messageError.textContent = `Message should be at least ${message.minLength} characters; you entered ${message.value.length}.`;
        }
    }

});

