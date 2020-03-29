$(document).ready(() => {
    const socket = io();
    checkMobile();
    socket.on('connect', function () {
        socket.emit('new_host');
    });
    socket.on('disconnect', function () {
        socket.emit('remove_host');
    });
});

function checkMobile() {
    if (isMobileDevice()) {
        location.href = "/mobile";
    } else {
        $('.mobile').html('no');
    }
}

function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}
