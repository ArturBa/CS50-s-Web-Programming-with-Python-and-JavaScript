$(document).ready(function () {
    $('#new-topic').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add-topic/',
            data: $(this).serialize(),
            success: function (data) {
                const json = $.parseJSON(data);
                console.log(json)
                location.pathname = `topic/${json.topic_id}`;
            }
        })
    })
})
