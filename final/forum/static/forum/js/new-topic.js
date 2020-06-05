$(document).ready(function () {
    $('#new-topic').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add-topic/',
            data: $(this).serialize(),
            success: function (data) {
                location.pathname = `topic/${data.topic_id}`;
            }
        })
    })
})
