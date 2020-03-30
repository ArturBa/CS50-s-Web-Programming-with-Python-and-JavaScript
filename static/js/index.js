checkMobile();

function checkMobile() {
    if (isMobileDevice()) {
        location.href = "/mobile";
    } else {
        location.href = "/desktop";
    }
}

function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}
