$(document).ready(() => {
    setInterval(newImage, 1000);
});

function httpImg() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", '/get_img', true); // false for synchronous request
    xmlHttp.send(null);
    console.log(xmlHttp.responseType);
    console.log(xmlHttp.responseURL);
    return xmlHttp.responseURL;
}


function newImage() {
    console.log('new image');
    $.ajax({
        url: '/get_img',
        processData: false,
    }).always(function (b64data) {
        console.log(b64data['img']);
        $('#img').attr("src", b64data['img']);
    });
}