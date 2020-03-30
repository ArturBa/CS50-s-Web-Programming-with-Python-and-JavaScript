function requestFullscreen() {
    let elem = document.getElementById("fullscreen");
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
    }
}

function startDrawing() {
    requestFullscreen();
    $('#fullscreen').load('/draw #fullscreen > *');
    console.log('hi there');

}