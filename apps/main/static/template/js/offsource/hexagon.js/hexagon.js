/**
 * hexagon.js - http://profenter.de/projekte/hexagon-js 0.4
 *
 * @author Profenter Systems / http://profenter.de/
 * @website http://profenter.de/projekte/hexagon-js
 */


/**
 *
 * @param scale
 * @param material
 * @returns {*}
 * @constructor
 */
THREE.Hexagon = function(scale, material) {
    if(typeof THREE === "undefined") {
        console.error("no Three.js found");
        return false;
    }
    var _this = this;
    this.i = 0;
    this.rotationValue  = this.positionValue = {
        x:0,
        y:0,
        z:0
    };
    this.position = function() {

    };
    this.rotation = function() {

    };
    this.geometry = new THREE.BoxGeometry(0, 0, 0);
    this.geometry_lines = new THREE.Geometry();
    this.line = '';
    this.debug = false;

    /*
     * given parameter
     */
    this.scale = scale;
    this.material = material;
    /**
     *
     */
    this.draw = function() {
        this.triangle(
            {x: 0.866 * this.scale, y: 0.5 * this.scale,    z: 0},
            {x: 0,                  y: 0,                   z: 0},
            {x: 0,                  y: this.scale,          z: 0}
        );
        this.triangle(
            {x: 0.866 * this.scale, y: 0.5 * this.scale,z: 0},
            {x: 0,                  y: this.scale,      z: 0},
            {x: 0.866 * this.scale, y: 1.5 * this.scale,z: 0}
        );
        this.triangle(
            {x: 0.866 * this.scale,     y: 0.5 * this.scale,z: 0},
            {x: 0.866 * this.scale,     y: 1.5 * this.scale,z: 0},
            {x: 0.866 * this.scale * 2, y: this.scale,      z: 0}
        );
        this.triangle(
            {x: 0.866 * this.scale,     y: 0.5 * this.scale,z: 0},
            {x: 0.866 * this.scale * 2, y: this.scale,      z: 0},
            {x: 0.866 * this.scale * 2, y: 0,               z: 0}
        );
        this.triangle(
            {x: 0.866 * this.scale,     y: 0.5 * this.scale,    z: 0},
            {x: 0.866 * this.scale * 2, y: 0,                   z: 0},
            {x: 0.866 * this.scale,     y: -0.5 * this.scale,   z: 0}
        );
        this.triangle(
            {x: 0.866 * this.scale, y:  0.5 * this.scale,   z: 0},
            {x: 0.866 * this.scale, y: -0.5 * this.scale,   z: 0},
            {x: 0,                  y: 0,                   z: 0}
        );
        this.log("creating hexagon...");
        this.Hexagon = new THREE.Mesh(this.geometry, this.material);
        this.Hexagon.flipSided = true;


        //this.Hexagon.position.set(this.position.x, this.position.y, this.position.z);
        //this.position.set(this.positionValue.x,this.positionValue.y,this.positionValue.z);
    };
    /**
     *
     * @param position1
     * @param position2
     * @param position3
     */
    this.triangle = function(position1, position2, position3) {
        var geometry = new THREE.Geometry(this.scale, this.scale, this.scale);
        geometry.vertices.push(new THREE.Vector3(position1.x, position1.y, position1.z));
        geometry.vertices.push(new THREE.Vector3(position2.x, position2.y, position2.z));
        geometry.vertices.push(new THREE.Vector3(position3.x, position3.y, position3.z));
        geometry.faces.push(new THREE.Face3(0, 2, 1));
        geometry.merge(this.geometry);
        this.geometry_lines.vertices.push(new THREE.Vector3(position2.x,position2.y, position2.z));

        if(this.i == 0) {
            this.geometry_lines_to_save = new THREE.Vector3(position2.x,position2.y, position2.z);
        } else if(this.i == 5) {
            this.geometry_lines.vertices.push(this.geometry_lines_to_save);
        }
        this.i = this.i+1;
    };
    /**
     *
     * @param x
     * @param y
     * @param z
     */
    this.position.set = function(x,y,z) {
        _this.positionValue.x = x;
        _this.positionValue.y = y;
        _this.positionValue.z = z;
        _this.log("setting position to: ");
        _this.log({
            x:_this.positionValue.x,
            y:_this.positionValue.y,
            z:_this.positionValue.z
        });
        _this.calc();
    };
    /**
     *
     * @param x
     * @param y
     * @param z
     */
    this.rotation.set = function(x,y,z) {
        _this.rotationValue.x = x;
        _this.rotationValue.y = y;
        _this.rotationValue.z = z;
        _this.log("setting rotation to: ");
        _this.log({
            x:_this.rotationValue.x,
            y:_this.rotationValue.y,
            z:_this.rotationValue.z
        });
        _this.calc();
    };

    /**
     * recalculates border and hexagon
     */
    this.calc = function() {
        /*
        Position
         */
        if(_this.line != null && typeof _this.line === 'object') {
            _this.line.position.set(this.positionValue.x, this.positionValue.y, this.positionValue.z);
        }
        _this.Hexagon.position.set(this.positionValue.x, this.positionValue.y, this.positionValue.z);
        /*
        * Rotation
         */
        if(_this.line != null && typeof _this.line === 'object') {
            _this.line.rotation.set(this.rotationValue.x, this.rotationValue.y, this.rotationValue.z);
        }
        _this.Hexagon.rotation.set(this.rotationValue.x, this.rotationValue.y, this.rotationValue.z);
    };

    /**
     * adds an border to the hexagon
     *
     * @param material Material of border
     * @returns {object|boolean}
     */
    this.border = function(material) {
        if(typeof _this.line !== 'object') {
            _this.line = new THREE.Line(_this.geometry_lines,material);
            _this.line.position.set(_this.positionValue.x, _this.positionValue.y, _this.positionValue.z);
        } else {
            if(material != null && typeof material === 'object') {
                _this.line.material = material;
            } else {
                return false;
            }
        }
        return _this.line;
    };

    /**
     *
     * @param text
     */
    this.log = function(text) {
        if (this.debug === true) {
            var namedTable = function(index, key) {
                this.Position = index;
                this.Value = key;
            };
            if(typeof text == "string") {
                console.info("Hexagon.js: " + text);
            } else if(typeof text == "object") {
                var table = {};
                for (var key in text) {
                    table[key] = new namedTable(key,text[key]);
                }
                console.table(table);
            }

        }
    };

    /***
     * Displays an info table in users console
     *
     * @param index
     * @param key
     */
    var about = function(index, key) {
        this.Name = index;
        this.Value = key;
    };

    /*
     * END about
     */

    if (typeof window.DEBUG !=  "undefined" && window.DEBUG === true) {
        this.debug = true;
    }

    this.draw();
    return this;
};
(function(){
    var s = window.location.search.substring(1).split('&');
    if(!s.length) return;
    window.$_GET = {};
    for(var i  = 0; i < s.length; i++) {
        var parts = s[i].split('=');
        //window.$_GET[unescape(parts[0])] = unescape(parts[1]);
        window.$_GET[encodeURI(parts[0])] = encodeURI(parts[1]);
    }
}());
(function(){
    if($_GET["debug"] == "true") {
         window.DEBUG = true;
    }
}());