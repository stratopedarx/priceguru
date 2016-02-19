jQuery.fn.multiselect = function() {
    $(this).each(function() {
        var checkboxes = $(this).find("input:checkbox");
        checkboxes.each(function() {
            var checkbox = $(this);
            // Highlight pre-selected checkboxes
            if (checkbox.prop("checked"))
                checkbox.parent().addClass("multiselect-on");

            // Highlight checkboxes that the user selects
            checkbox.click(function() {
                if (checkbox.prop("checked"))
                    checkbox.parent().addClass("multiselect-on");
                else
                    checkbox.parent().removeClass("multiselect-on");
            });
        });
    });
};




$(document).ready(function() {
    $('#search,#search2').on('keyup', function() {
        var value = $(this).val();
        var regexp = new RegExp(value, 'im');
        var $opts = $(this).parents('.col').find('select option');
        $($opts).filter(function(n, option) {
            var found = option.innerHTML.search(regexp) > -1;
            option.style.display = !found ? 'none' : 'block';

            return found;
        })
    });
    $('.editbutton').click(function() {
        var prev = $(this).data('prevStatus');
        $('#content').prop('contentEditable', !prev).focus();
        $('#body h3').prop('contentEditable', !prev);
        $(this).data('prevStatus', !prev)
    });

    $('._save').click(function() {
        $('#content,#body h3').prop('contentEditable', false)
        alert('save')
    });

    $("select").mousedown(function(e){
        e.preventDefault();

        var scroll = this.scrollTop;

        e.target.selected = !e.target.selected;

        this.scrollTop = scroll;

        $(this).focus();
    }).mousemove(function(e){
        e.preventDefault()
    });

});