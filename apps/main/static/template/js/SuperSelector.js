(function ($) {

    $.fn.SuperSelector = function (options) {
        console.log('SuperSelector', options);
        var self = this;

        options = options || {};
        options = $.extend({
            defaultValue: null
        }, options);

        return this.each(function() {
            self.init.call($(this), options)
        });
    };

    $.fn.SuperSelector.prototype.init = function (el, params) {
        var self = this;

        this.$el = $(el);
        this.$input = $('input', this.$el);
        this.$input.bind("change paste keyup", function() {
            console.log($(this).val());
        });
        this.$submenu = $('.submenu', this.$el);
        $('li', this.$submenu).on('click', function (event) {
            var current = $(event.currentTarget).text();
            //console.log('current', current);
            self.$input.val(current);
            //self.$submenu.hide();
            return false;
        });

        if (params) {
            if (params.hasOwnProperty('defaultValue')) {
                console.log('default', params['defaultValue'])
            }
        }

        if(options.defaultValue) {
            this.$input.val(options.defaultValue)
            //this.$input.attr('placeholder', options.defaultValue)
        }

        this.$input.on('focus', function (event) {
            console.info('focus', event, self.$submenu, $(self.$input).val())

            if($(self.$input).val() == options.defaultValue) {
                $(self.$input).val('').focus()
            }
            //self.$input, $(self.$input).val(), options.defaultValue)
            self.$submenu.show();
        });
        this.$input.on('focusout', function (event) {
            //console.log('focusout', event.target, $(self.$input).val(), options.defaultValue)
            if($(self.$input).val() == '') {
                $(self.$input).val(options.defaultValue)
            }

            window.setTimeout(function() {
                self.$submenu.hide();
            }, 100);
        });
        this.$input.on('blur', function (event) {
            console.log('blur', event.target)
            //self.$submenu.hide();
        });

        this.$el.on('keyup', function (event) {
            var input_value = $('input', event.currentTarget).val();

            $('li', this.$submenu).hide().filter(function (n, el) {
                var text = $(el).text().toString().toLowerCase();
                return text.search(input_value, 'img') > -1;
            }).show()
        });
    };

})(jQuery);

/*$(document.body).click(function(event) {
 /!*console.log('click', {
 'self.$input': self.$input,
 'event.target': event.target,
 'event.target.nodeName': event.target.nodeName,
 '$(event.target)': $(event.target),
 '==': $(event.target) == self.$input
 });*!/
 event.preventDefault();
 if(event.target.nodeName == 'INPUT') {
 console.log('event.target', event.target)
 self.$submenu.show();
 } else {
 self.$submenu.hide();
 }

 //document.body.focus();
 return false;
 });*/