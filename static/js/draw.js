function getCanvas() {
    startup();
    canvas = document.getElementById('canvas');
    let rect = canvas.parentNode.getBoundingClientRect();
    canvas.width = rect.height;
    canvas.height = rect.width;
    positionOffset = findPos(canvas);
    ctx = canvas.getContext('2d');
    setInterval(updateTimer, 1000);

    $('circle').each(function () {
        $(this).on('click', function () {
            color = $(this).data('color');
        })
    })
}

$('canvas').onclick(function () {
    if ($(this) === null){
        getCanvas();
    }
});

let color = 'black';
const MAX_TIME = 30; // max time of drawing in seconds
const LINE_WIDTH = 10; // max time of drawing in seconds
let canvas;
let ctx;
let positionOffset;
let currTime = 0;

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

let prevPoint;
let currPoint = 0;

function startup() {
    const el = document.body;
    el.addEventListener("touchstart", handleStart, false);
    el.addEventListener("touchend", handleEnd, false);
    el.addEventListener("touchmove", handleMove, false);
    // el.addEventListener("touchcancel", handleCancel, false);
    // el.addEventListener("touchleave", handleEnd, false);
}


function updateTouchPosition(event) {
    const touch = event.changedTouches[0];
    prevPoint = currPoint;
    currPoint = new Point(parseInt(touch.clientY) - positionOffset.x,
        window.innerWidth - parseInt(touch.clientX) - positionOffset.y);
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

function log(msg) {
    // var p = document.getElementById('log');
    // p.innerHTML = msg + "\n";
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
}

function clearCanvas() {
    // #F8ECC2

}