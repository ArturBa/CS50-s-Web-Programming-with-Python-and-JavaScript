$(document).ready(() => {
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.add-menu').forEach(button => {
        button.onclick = () => {
            console.log('hi');
            $.ajax({
                type: 'POST',
                url: 'add/pizza/',
                data: {
                    name: 'artur',
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function () {
                    console.log('add success');
                }
            });
        };
    });

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
