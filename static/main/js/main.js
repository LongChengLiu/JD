$('.carousel').carousel({
    interval: 2000
});


// 最后加载
$(document).ready(function () {
    var myTouch = util.toucher(document.getElementById('carousel-example-generic'));
    myTouch.on('swipeLeft', function (e) {
        $('#right').click();
    }).on('swipeRight', function (e) {
        $('#left').click();
    });
});