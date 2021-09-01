function hideBoxData($element) {
    $box = $('#view-box-information');
    $box.css('opacity', '0');
    $box.slideUp(250);
    $('.box-data-hide').show(500);
    $('.box-data-show').hide(300);


    $element.toggleClass('collapse-box-data expand-box-data');
}

function showBoxData($element) {
    $box = $('#view-box-information');
    $box.slideDown(250);
    $box.css('opacity', '1');
    $('.box-data-hide').hide(300);
    $('.box-data-show').show(500);

    $element.toggleClass('expand-box-data collapse-box-data');
}
$(function () {
    $('.expand-box-data, .collapse-box-data').on('click', function () {
        if ($(this).hasClass('collapse-box-data'))
            hideBoxData($(this));
        else if ($(this).hasClass('expand-box-data'))
            showBoxData($(this));
    })
})