(function () {
    // Calculate the full document height.
    function getHeight() {
        return Math.max(
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight,
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.body.clientHeight
        );
    }

    // Send the current height to the embedding page.
    function sendHeight() {
        var height = getHeight();

        parent.postMessage(
            {
                type: "iframeHeight",
                height: height,
                origin: window.location.origin,
                url: window.location.href,
            },
            "*"
        );

        console.log("Iframe height sent to parent:", height + "px");
    }

    if (document.readyState === "complete") {
        sendHeight();
    } else {
        window.addEventListener("load", sendHeight);
    }

    window.addEventListener("resize", function () {
        clearTimeout(window.resizeTimer);
        window.resizeTimer = setTimeout(sendHeight, 100);
    });

    if (window.MutationObserver) {
        var observer = new MutationObserver(function () {
            sendHeight();
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
        });
    }
})();
