$(document).ready(function () {
    $('#new-post').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/new-post/',
            data: $('#new-post').serialize(),
            success: function () {
                location.reload();
            }
        })
    })
})
