let color = 'black';
const MAX_TIME = 45; // max time of drawing in seconds
const LINE_WIDTH = 10; // drawing line width
let canvas;
let ctx;
let positionOffset;
let currTime = 0;

function setUpCanvas() {
    canvas = document.getElementById('canvas');
    canvas.width = window.innerHeight;
    canvas.height = window.innerWidth - 2 * (10 + 40) - 4 * 5;
    positionOffset = findPos(canvas);
    ctx = canvas.getContext('2d');
    clearCanvas();

    $('circle').each(function () {
        $(this).on('click', function () {
            color = $(this).data('color');
        })
    })
}

function setUpEvents() {
    const el = document.body;
    el.addEventListener("touchstart", handleStart, false);
    el.addEventListener("touchend", handleEnd, false);
    el.addEventListener("touchmove", handleMove, false);
    // el.addEventListener("touchcancel", handleCancel, false);
    el.addEventListener("touchleave", handleEnd, false);
}

let prevPoint;
let currPoint = 0;

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

function updateTouchPosition(event) {
    const touch = event.changedTouches[0];
    prevPoint = currPoint;
    currPoint = new Point(parseInt(touch.clientX) - positionOffset.x,
        parseInt(touch.clientY) - positionOffset.y);
}


function handleStart(event) {
    updateTouchPosition(event);
    ctx.beginPath();
    ctx.arc(currPoint.x, currPoint.y, LINE_WIDTH / 2, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
}

function handleEnd(event) {
    updateTouchPosition(event);
    prevPoint = 0;
}

function handleMove(event) {
    updateTouchPosition(event);
    ctx.beginPath();
    ctx.moveTo(prevPoint.x, prevPoint.y);
    ctx.lineTo(currPoint.x, currPoint.y);
    ctx.lineWidth = LINE_WIDTH;
    ctx.strokeStyle = color;
    ctx.stroke();
}


function findPos(obj) {
    var curleft = 0,
        curtop = 0;

    if (obj.offsetParent) {
        do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);

        return {x: curleft - document.body.scrollLeft, y: curtop - document.body.scrollTop};
    }
}

function updateTimer() {
    currTime += 1;
    $('.load').css('width', `${currTime * 100 / MAX_TIME}%`);
    if (currTime === MAX_TIME) {
        sendImage();
        clearCanvas();
        currTime = 0;
    }
}

function clearCanvas() {
    ctx.fillStyle = "#E2DAD5";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}


function sendImage() {
    const imgURL = canvas.toDataURL();
    $.ajax({
        type: "POST",
        url: "/save_img",
        data: {
            'img64': imgURL
        },
    }).done(() => {
        location.reload();
    });
}


function start() {
    openFullscreen();
    screen.orientation.lock("landscape");
    setUpEvents();
    setUpCanvas();
    $('#start').remove();
    setInterval(updateTimer, 1000);
}

function openFullscreen() {
    const elem = document.getElementById('fullscreen');
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
