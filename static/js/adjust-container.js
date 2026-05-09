(function(){
    function adjustContainerOffset() {
        try {
            var nav = document.querySelector('nav');
            var root = document.documentElement;
            if (!nav || !root) return;
            var navHeight = nav.offsetHeight || 0;
            root.style.setProperty('--container-top-offset', (navHeight + 10) + 'px');
        } catch (err) {
            console && console.warn && console.warn('adjustContainerOffset error', err);
        }
    }

    // Observe changes to nav (useful if menu expands/collapses)
    var nav = document.querySelector('nav');
    if (nav && window.MutationObserver) {
        var mo = new MutationObserver(function(){
            adjustContainerOffset();
        });
        mo.observe(nav, { attributes: true, childList: true, subtree: true });
    }

    window.addEventListener('load', adjustContainerOffset);
    window.addEventListener('resize', adjustContainerOffset);
})();
