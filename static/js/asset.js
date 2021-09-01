/**
 * Nasconde le informazioni del box.
 * @param {HTMLDivElement} $element Pulsante premuto dall'utente.
 */
function hideBoxData($element) {
    $('#view-box-information').slideUp();
    $('.box-data-hide').show(500);
    $('.box-data-show').hide(300);

    $element.toggleClass('collapse-box-data expand-box-data');
}

/**
 * Mostra le informazioni del box.
 * @param {HTMLDivElement} $element Pulsante premuto dall'utente.
 */
function showBoxData($element) {
    $('#view-box-information').slideDown();
    $('.box-data-hide').hide(500);
    $('.box-data-show').show(300);

    $element.toggleClass('expand-box-data collapse-box-data');
}

function assetDeleteSuccess(data, $item) {
    $item.html('<h6 class="font-6 site-red-text">' +
        '<i class="fas fa-times"></i>&nbsp;Eliminato' +
        '</h6>'
    )
}

function assetMoveSuccess(data, $item) {
    $item.html('<h6 class="font-6 site-blue-text">' +
        '<i class="fas fa-check"></i>&nbsp;Spostato' +
        '</h6>'
    )
}

$(function () {
    /** Event listener on click del pulsante per lo show/hide delle informazioni. */
    $('.collapse-box-data, .expand-box-data').on('click', function () {
        if ($(this).hasClass('collapse-box-data'))
            hideBoxData($(this));
        else if ($(this).hasClass('expand-box-data'))
            showBoxData($(this));
    });

    $('.text-show-more').on('click', function () {
        $('#text-show-more-modal').modal('show');
    });

    $('#close-show-more-modal').on('click', function () {
        $('#text-show-more-modal').modal('hide');
    });

    $('.delete-asset').on('click', function () {
        ajaxDeleteAsset($(this).attr('data-post-id'), $(this))
    })

    $('.move-asset').on('click', function () {
        let asset_pk = $(this).closest('.asset-actions-root').
            find('.move-asset-root').attr('data-post-id');
        ajaxMoveAsset(asset_pk, $(this).attr('data-post-id'), $(this))
    })
});