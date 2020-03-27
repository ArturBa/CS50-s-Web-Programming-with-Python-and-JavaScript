$(document).ready(() => {
    update_Prices();
    $('.large').change(() => {
        update_Prices();
    });
});

function update_Prices() {
    $('.item-cart').each(function () {
        console.log($(this).find(".large").prop('checked'));
        if ($(this).find(".large").prop('checked')) {
            $(this).find('.price').html($(this).find('.price-large').html());
        } else {
            $(this).find('.price').html($(this).find('.price-small').html());
        }
    });
}