$(document).ready(() => {
    update_Prices();
    $('input').change(() => {
        update_Prices();
    });
});

function update_Prices() {
    $('.item-cart').each(function () {
        if ($(this).find(".large").prop('checked')) {
            $(this).find('.price').html($(this).find('.price-large').html());
        } else {
            $(this).find('.price').html($(this).find('.price-small').html());
        }
        if ($(this).find('.extra-cheese').prop('checked')) {
            $(this).find('.price').html(parseFloat($(this).find('.price').html()) + 0.5);
        }
        let add_price = 0;
        $(this).find('.adds').each(function () {
            for (let i in $(this).val()) {
                add_price += 0.5;
            }
        });
        $(this).find('.price').html(parseFloat($(this).find('.price').html()) + add_price);
        $(this).find('.price').html(parseFloat($(this).find('.price').html()) * parseFloat($(this).find('.quantity').val()));
    });
    update_total();
}

function update_total() {
    let total = 0;
    $('.price').each(function () {
        total += parseFloat($(this).html());
    });
    $('.total-price').html(total.toFixed(2));
}

function checkout() {
    $('form').each(function () {
        const url = $(this).attr('action');
        const fd = new FormData($(this)[0]);
        $.ajax({
            type: "POST",
            url: url,
            data: fd,
            processData: false,
            contentType: false,
            success: function (data, status) {
                //this will execute when form is submited without errors
            },
            error: function (data, status) {
                //this will execute when get any error
            },
        });
    });
    return false;
}

$(document).ajaxStop(function () {
    location.replace('/checkout');
});