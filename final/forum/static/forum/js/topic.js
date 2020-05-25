$(document).ready(function () {
    $('#new-post').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/new-post/',
            data: $('#new-post').serialize(),
            success: function () {
                location.reload();
            }
        })
    })
    $('.votes-form').each(function () {
        $(this).submit(function (event) {
            event.preventDefault();
            console.log(`add: ${$(this).serialize()}`)
            $.ajax({
                type: 'POST',
                url: '/add-point/',
                data: $(this).serialize(),
            })
        })
    })
    set_scroll();
    bold_curr_loc();
})

function set_scroll() {
    const max_page = Number($('#max-page').html());
    const page = get_curr_loc();
    const scroll = $('#post-scroller')
    const topic = get_topic_id();

    if (page > 2) {
        scroll.append(`<a href='/topic/${topic}' class='page-scroll' id='page-0'>0 ...</a>`)
    }
    for (let i = -2; i < 3; i++) {
        if (page + i >= 0 && page + i <= max_page) {
            scroll.append(`<a href='/topic/${topic}?page=${page + i}' class='page-scroll' id='page-${page + i}'>${page + i}</a>`)
        }
    }
    if (page < max_page - 2) {
        scroll.append(`<a href='/topic/${topic}?page=${max_page}' class='page-scroll' id='page-${max_page}'>... ${max_page}</a>`)
    }
}

function bold_curr_loc() {
    const page = get_curr_loc();
    $(`#page-${page}`).css('font-weight', 'bold');
}

function get_curr_loc() {
    let params = new URLSearchParams(document.location.search.substring(1));
    return Number(params.get('page') ? params.get('page') : 0);
}

function get_topic_id() {
    return Number($('#topic-id').html());
}
