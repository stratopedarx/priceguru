var Semantic_net_events = function(renderer, camera) {
    this.renderer = renderer;
    this.camera = camera;
    this._initMouse();

    window.addEventListener('resize', this.onWindowResize.bind(this), false);
    document.addEventListener('mousemove', this.onDocumentMouseMove.bind(this), false);
    //document.addEventListener('mousedown', this.onDocumentMouseDown.bind(this), false);
    document.addEventListener('click', this.onDocumentMouseDown.bind(this), false);
}

Semantic_net_events.prototype._initMouse = function() {
    this.mouse = new THREE.Vector2();
}

Semantic_net_events.prototype._clickable = [];
Semantic_net_events.prototype.setOnClick = function (obj, cb) {
    this._clickable.push(obj);

    obj.click = cb.bind(obj);
}

Semantic_net_events.prototype._hoverable = [];
Semantic_net_events.prototype.setOnHover = function (obj, onHover, onUnHover) {
    this._hoverable.push(obj);

    obj.hover = onHover;
    if (onUnHover)
        obj.unhover = onUnHover;
}

Semantic_net_events.prototype.onWindowResize = function () {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();

    //this.renderer.shadowMapEnabled = true;
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this._initMouse();
}

Semantic_net_events.prototype.onDocumentMouseMove = function (event) {
    event.preventDefault();

    this.mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
    this.mouse.y = -( event.clientY / window.innerHeight ) * 2 + 1;
    //console.log({x: this.mouse.x, y: this.mouse.y})
    var vector = new THREE.Vector3(this.mouse.x, this.mouse.y, 0.5)//.unproject(this.camera);
    var raycaster = new THREE.Raycaster(this.camera.position, vector.sub(this.camera.position).normalize());
    var intersects = raycaster.intersectObjects(this._hoverable);

    if (intersects.length > 0) {
        var SELECTED = intersects[0].object;

        if (SELECTED.hover && SELECTED !== this.prev_hover) {
            this.prev_hover = SELECTED;

            SELECTED.hover.apply(SELECTED, [event])
        }
        if (this.prev_hover && this.prev_hover != SELECTED && this.prev_hover.unhover) {
            this.prev_hover.unhover.apply(this.prev_hover, [event])
            this.prev_hover = null
        }
    } else {
        /*if (this.prev_hover && this.prev_hover.unhover) {
         this.prev_hover.unhover.apply(this.prev_hover, [event])
         }*/
    }
}

Semantic_net_events.prototype.onDocumentMouseDown = function (event) {
    event.preventDefault();
    var vector = new THREE.Vector3(this.mouse.x, this.mouse.y, 0.5).unproject(this.camera);
    var raycaster = new THREE.Raycaster(this.camera.position, vector.sub(this.camera.position).normalize());
    //console.log('this.clickable', this._clickable)
    var intersects = raycaster.intersectObjects(this._clickable);

    if (intersects && intersects.length > 0) {
        var SELECTED = intersects[0].object;
        if (SELECTED.click) {
            SELECTED.click.apply(SELECTED, [event]);
            //SELECTED.click(SELECTED, event)
        }
    }
}