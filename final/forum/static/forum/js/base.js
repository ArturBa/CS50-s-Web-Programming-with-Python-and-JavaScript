$(document).ready(function () {
    $('#login').submit(function (event) {
        console.log('trying to login');
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/login/',
            data: $('#login').serialize(),
            success: function () {
                location.reload();
            },
            statusCode: {
                401: function () {
                    alert('Invalid credentials');
                }
            }
        });
    });
    $('#logout').click(function (event) {
            event.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/logout/',
                data: $('#logout-token').serialize(),
                success: function () {
                    location.reload();
                }
            });
        }
    );
})

