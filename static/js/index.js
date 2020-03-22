if (localStorage.getItem('username')) {
    let chat_id = localStorage.getItem('chat');
    location.replace(`/chat/${chat_id}`);
}

document.addEventListener('DOMContentLoaded', () => {
        const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
        const username = document.getElementById('username');
        const usernameError = document.querySelector('span.error');

        // When connected, configure buttons
        socket.on('connect', () => {

            document.getElementById('new-user').addEventListener('submit', function (event) {
                // prevent the form from being sent by canceling the event
                event.preventDefault();
                // if the username field is valid, we let the form submit
                if (!username.validity.valid) {
                    // If it isn't, we display an appropriate error message
                    showError();
                } else {
                    // If is valid we add a new user
                    socket.emit('add user', {'username': username.value});
                }
            });

            socket.on("user created", data => {
                localStorage.setItem('username', data.username);
                localStorage.setItem('chat', 'global');
                location.replace('/chat/global');
            });

        });

        username.addEventListener('input', () => {
            // Each time the user types something, we check if the
            // form fields are valid.

            if (username.validity.valid) {
                // In case there is an error message visible, if the field
                // is valid, we remove the error message.
                usernameError.innerHTML = ''; // Reset the content of the message
                usernameError.className = 'error'; // Reset the visual state of the message
            }
        });

        function showError() {
            if (username.validity.valueMissing) {
                // If the field is empty
                // display the following error message.
                usernameError.textContent = 'You need to enter a username.';
            } else if (username.validity.tooShort) {
                // If the data is too short
                // display the following error message.
                usernameError.textContent = `Username should be at least ${username.minLength} characters; you entered ${username.value.length}.`;
            }
        }

        usernameError.className = 'error active';
    }
);
