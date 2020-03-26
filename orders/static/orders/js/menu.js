$(document).ready(() => {
    const csrftoken = getCookie('csrftoken');
    const notification = $('.notification');

    document.querySelectorAll('.add-menu').forEach(button => {
        button.onclick = () => {
            console.log(button.dataset.large);
            $.ajax({
                type: 'POST',
                url: 'add/',
                data: {
                    type: button.dataset.type,
                    id: button.dataset.id,
                    large: button.dataset.large,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function () {
                    console.log('add success');
                    notification.addClass('show');
                    setTimeout(() => {
                        notification.removeClass('show');
                    }, 2500);

                }
            });
        };
    });

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
