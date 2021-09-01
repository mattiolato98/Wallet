window.onscroll = window.screen.width > 991 ? function() {scrollFunction()} : null;
function scrollFunction() {
    if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
        $("#site-navbar").css('padding-bottom', '5px');
        $("#site-navbar .logo-font").css('font-size', '25px');
    } else {
        $("#site-navbar").css('padding-bottom', '120px');
        $("#site-navbar .logo-font").css('font-size', '40px');
    }
}

$(function () {
    let clicked = false;

    $('.burger').on('click', function () {
        if (!clicked) {
            $('#site-navbar').css('background', '#242424');
            clicked = true;
            $(this).toggleClass('toggle');
            $('#navbarSupportedContent').toggle(250);
            setTimeout(function (){clicked = false;}, 250);
            $('#site-navbar').toggleClass('navbar-image-background');
        }
    });

    $(document).mouseup(function (e) {
        if (window.screen.width < 992) {
            const container = $("#site-navbar");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                $('#navbarSupportedContent').hide(250);
                $('.burger').removeClass('toggle');
            }
        }
    });
});