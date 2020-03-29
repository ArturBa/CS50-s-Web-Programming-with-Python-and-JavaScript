checkMobile();

function checkMobile() {
    if (isMobileDevice()) {
        location.href = "/draw";
    } else {
        $('.mobile').html('no');
    }
}

function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}
