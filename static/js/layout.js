if (!localStorage.getItem('username')) {
    location.replace(`/`);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('hello-user').innerHTML = `Hi ${localStorage.getItem('username')}`;
    document.getElementById('chat-head').innerHTML = `:${localStorage.getItem('chat')}`;
    document.querySelector('title').innerHTML = `:${localStorage.getItem('chat')}`;
});

