$(document).ready(() => {
    $('.content').removeClass('col-md-9');
    $('footer').remove();
    $('nav').remove();

    setInterval(update, 2000);
});

function submitForm(event) {
    const form = event.target;
    event.preventDefault();
    const url = form.action;
    const data = new FormData(form);

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        processData: false,
        contentType: false,
        dataType: "json",
        success: function () {
            form.remove()
        }
    });
    return false;
}

function update() {
    $('.collecting').load('/orders .collecting > *');
    $('.cooking').load('/orders .cooking > *');
    $('.delivering').load('/orders .delivering > *');
    $('.completed').load('/orders .completed > *');
}
