if (!localStorage.getItem('username')) {
    location.replace(`/`);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('hello-user').innerHTML = `Hi ${localStorage.getItem('username')}`;
    document.querySelector('title').innerHTML = `:${localStorage.getItem('chat')}`;

    document.getElementById('mode').onchange = function () {
        if (this.checked === true) {
            document.querySelector('body').classList.add('dark-mode');
        } else {
            document.querySelector('body').classList.remove('dark-mode');
        }
    }
});

// $('#mode').change(function(){
//
//     if ($(this).prop('checked'))
//     {
//         $('body').addClass('dark-mode');
//     }
//     else
//     {
//         $('body').removeClass('dark-mode');
//     }
//
// });