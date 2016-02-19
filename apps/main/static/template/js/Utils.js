var Utils = {
    deg2rad: function (angle) {
        return angle * .017453292519943295; // (angle / 180) * Math.PI;
    },
    getRandomColor: function () {
        return '0x' + Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase()
    },
    getBody: function() {
        return document.body || document.getElementsByTagName('body')[0];
    },
    debugColors: function() {
        var args = Array.prototype.slice.call(arguments);

        for(var i in args) {
            var color = parseInt(args[i]).toString(16).toUpperCase();
            console.log(args[i], color);
            console.log("%c"+color, "background-color:"+color);
        }
    }
}