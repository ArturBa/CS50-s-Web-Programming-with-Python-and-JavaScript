$(document).ready(() => {
    const location = window.location.href.substr(window.location.href.indexOf('/', 10));

    // remove active class from all
    $(".navbar .nav-item").removeClass('active');

    // add active class to div that matches active url
    $(".nav-item a[href='" + location + "']").addClass('active');
    $('.navbar-nav li').click(function () {
        $('.navbar li').removeClass('active');
        $(this).addClass('active');
    });
});

