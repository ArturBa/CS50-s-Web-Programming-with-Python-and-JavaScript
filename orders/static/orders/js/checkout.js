$(document).ready(() => {
    update_subs();
    update_total();
});

function update_subs() {
    $('.checkout-item').each(function () {
        if ($(this).find('.extra-cheese')) {
            $(this).find('.price').html(
                parseFloat($(this).find('.price').html()) + 0.5
            );
        }
        if (parseFloat($(this).find('.add-count').html())) {
            $(this).find('.price').html(
                parseFloat($(this).find('.price').html()) + 0.5 * parseFloat($(this).find('.add-count').html())
            );
        }
    });
}

function update_total() {
    let total = 0;
    $('.price').each(function () {
        total += parseFloat($(this).html());
    });
    $('.total-price').html(total.toFixed(2));
}
