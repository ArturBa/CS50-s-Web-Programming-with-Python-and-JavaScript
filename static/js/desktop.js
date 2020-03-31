$(document).ready(() => {
    const socket = io();
    await_text = $('#img').html();

    socket.on('connect', () => {
        socket.on('new img', () => {
            newImage();
        });

    })
});

function newImage() {
    $.ajax({
        url: '/get_img',
        processData: false,
    }).always(function (b64data) {
        $('#img').html(`<img alt="${await_text}"></img>`);
        $('img').attr("src", b64data['img']);
    });
}