$(function() {
    var $c = $('#carousel'),
        $w = $(window);

    $c.carouFredSel({
        align: false,
        items: 6,
        scroll: {
            items: 1,
            duration: 2000,
            timeoutDuration: 0,
            easing: 'linear',
            pauseOnHover: 'immediate'
        }
    });


    $w.bind('resize.example', function() {
        var nw = $w.width();
        if (nw < 990) {
            nw = 990;
        }

        $c.width(nw * 3);
        $c.parent().width(nw);

    }).trigger('resize.example');

});


var totalItems = $('#InternationalDelegationSlider .item').length;
var currentIndex = $('#InternationalDelegationSlider div.active').index() + 1;
$('.num').html(''+currentIndex+' OF '+totalItems+'');

$('#InternationalDelegationSlider').bind('slide.bs.carousel', function() {
    currentIndex = $('#InternationalDelegationSlider div.active').index() + 1;
    $('.num').html(''+currentIndex+' OF '+totalItems+'');
});


