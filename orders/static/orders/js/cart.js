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
        $(this).find('.price').html(parseFloat($(this).find('.price').html()) * parseFloat($(this).find('.quantity').val()));
    });
    update_total();
}

function update_total() {
    let total = 0;
    $('.price').each(function () {
        total += parseFloat($(this).html());
    });
    $('.total-price').html(total);
}