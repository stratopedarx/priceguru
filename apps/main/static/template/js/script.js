console.log('script.js')
THREE.warn = function(){};

function toggleFullScreen(elem) {
    // ## The below if statement seems to work better ## if ((document.fullScreenElement && document.fullScreenElement !== null) || (document.msfullscreenElement && document.msfullscreenElement !== null) || (!document.mozFullScreen && !document.webkitIsFullScreen)) {
    if ((document.fullScreenElement !== undefined && document.fullScreenElement === null) || (document.msFullscreenElement !== undefined && document.msFullscreenElement === null) || (document.mozFullScreen !== undefined && !document.mozFullScreen) || (document.webkitIsFullScreen !== undefined && !document.webkitIsFullScreen)) {
        if (elem.requestFullScreen) {
            elem.requestFullScreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullScreen) {
            elem.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}

//multiselect для выбора нескольких option у select:multiple без ctrl
jQuery.fn.multiselect = function () {
    $(this).each(function () {
        var checkboxes = $(this).find("input:checkbox");
        checkboxes.each(function () {
            var checkbox = $(this);
            // Highlight pre-selected checkboxes
            if (checkbox.prop("checked"))
                checkbox.parent().addClass("multiselect-on");

            // Highlight checkboxes that the user selects
            checkbox.click(function () {
                if (checkbox.prop("checked"))
                    checkbox.parent().addClass("multiselect-on");
                else
                    checkbox.parent().removeClass("multiselect-on");
            });
        });
    });
};

$(document).ready(function () {
    var canvas = document.getElementById('canvas');
    var Net = new SemanticNet(canvas);

    $('#plus').click(Net.onPlusClick.bind(Net));
    $('#minus').click(Net.onMinusClick.bind(Net));
    $('#size100').click(Net.on100Click.bind(Net));

    $('#fs').click(function () {
        document.getElementById("body").requestFullScreen()
        return false;
    });

    $('.selector1').SuperSelector({defaultValue: 'Поиск'});
    $('.selector2').SuperSelector({defaultValue: 'Поиск2'});

    $('.btn-group > button').click(function () {
        console.log('click', arguments)
        $(this).parent().find('.active').removeClass('active');
        $(this).addClass('active');
    });
});
