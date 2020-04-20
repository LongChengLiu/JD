!(function (n) {
    let e = n.document,
        t = e.documentElement,
        i = 750,
        d = i / 100,
        o = 'orientationchange' in n ? 'orientationchange' : 'resize',
        a = function () {
            let n = t.clientWidth || 320
            n > 750 && (n = 750)
            t.style.fontSize = n / d + 'px'
        }
    e.addEventListener &&
    (n.addEventListener(o, a, !1),
        e.addEventListener('DOMContentLoaded', a, !1))
})(window);

