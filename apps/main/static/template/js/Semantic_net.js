var SemanticNet = function (container) {
    $('.selector2 .glyphicon-remove').click(function() {
        $(this).parent().find('input:text').val('')
    });

    this.debug = true;
    this.scene = new THREE.Scene();

    var SCREEN_WIDTH = window.innerWidth,
        SCREEN_HEIGHT = window.innerHeight;
// CAMERA
    var VIEW_ANGLE = 45,
        ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT,
        NEAR = 0.1,
        FAR = 20000;
    this.camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);
    //this.camera = new THREE.OrthographicCamera(/*VIEW_ANGLE, ASPECT, NEAR, FAR*/);
    this.scene.add(this.camera);
    this.camera.position.set(350, 350, 250);
    this.camera.lookAt(this.scene.position);
// RENDERER
    this.renderTo = this.body;
    this.renderer = Detector.webgl ? new THREE.WebGLRenderer({antialias: true, alpha: true }) : new THREE.CanvasRenderer();
    if(container) {
        //console.log('setSize', $(container).innerWidth(), $(container).innerHeight())
        this.renderer.setSize($(container).innerWidth(), $(container).innerHeight());
    } else {
        this.renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
    }
    this.renderer.autoClear = false;
    this.renderer.gammaInput = true;
    this.renderer.gammaOutput = true;
    this.container = container || document.body;
    this.container.appendChild(this.renderer.domElement);
// EVENTS
    THREEx.WindowResize(this.renderer, this.camera);
    THREEx.FullScreen.bindKey({charCode: 'f'.charCodeAt(0)});
    this.body = Utils.getBody();

    this.addGuiControls();

    // CONTROLS
    this.vcontrols = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    //this.vcontrols = new THREE.TrackballControls(this.camera, this.renderer.domElement);
    // STATS
    if(this.debug) {
        this.stats = new Stats();
        this.stats.domElement.style.position = 'absolute';
        this.stats.domElement.style.bottom = 0;
        this.stats.domElement.style.zIndex = 100;
        this.container.appendChild(this.stats.domElement);

        // axes
        //this.scene.add(new THREE.AxisHelper(500));
    }

    // LIGHT
    //var light = new THREE.PointLight(0xffffff);
    //light.position.set(0, 250, 0);
    //this.scene.add(light);
    // FLOOR
    var floorTexture = new THREE.ImageUtils.loadTexture(this.textures.floor);
    floorTexture.wrapS = floorTexture.wrapT = THREE.RepeatWrapping;
    floorTexture.repeat.set(10, 10);
    var floorMaterial = new THREE.MeshBasicMaterial({map: floorTexture, side: THREE.DoubleSide});
    var floorGeometry = new THREE.PlaneBufferGeometry(200, 200, 10, 10);
    var floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.position.y = -0.5;
    floor.rotation.x = Math.PI / 2;
    //this.scene.add(floor);



    var skyGeometry = new THREE.BoxGeometry(5000, 5000, 5000);

    var materialArray = [
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.xpos)}),
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.xneg)}),
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.ypos)}),
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.yneg)}),
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.zpos)}),
        new THREE.MeshBasicMaterial({side: THREE.BackSide, map: THREE.ImageUtils.loadTexture(this.textures.bg.zneg)})
    ];

    var skyMaterial = new THREE.MeshFaceMaterial(materialArray);
    var skyBox = new THREE.Mesh(skyGeometry, skyMaterial);
    //this.scene.add(skyBox);
    var first_title = $(document).attr('title');
    THREE.DefaultLoadingManager.onProgress = function ( item, loaded, total ) {
        //console.log( item, loaded, total, ~~loaded/total );
        var title = ~~(100*loaded/total);
        console.log(title + '%')
        $('#loading').html(title + '%')
        //$().attr('title', (title>=100) ? first_title : title+'%')
    };
    this.events = new Semantic_net_events(this.renderer, this.camera);

    Semantic_api.getNodes(function(nodes) {
        console.log('getNodes', arguments);
        this.data = nodes;

        this.initObjects();
        this.animate();
    }.bind(this));
    /*$.getJSON('json/nodes.json', function(nodes) {
        this.data = nodes.results;

    }.bind(this));*/
}
SemanticNet.prototype.OPTIONS = {
    TRIANGLE_SIZE: 30,
    PYRAMYD_SIZE: 5
}
SemanticNet.prototype.textures = {
    floor: '../static/img/checkerboard.jpg',
    bg: {
        xpos: "../static/img/dawnmountain-xpos.png",
        xneg: "../static/img/dawnmountain-xneg.png",
        ypos: "../static/img/dawnmountain-ypos.png",
        yneg: "../static/img/dawnmountain-yneg.png",
        zpos: "../static/img/dawnmountain-zpos.png",
        zneg: "../static/img/dawnmountain-zneg.png"
    }
}
SemanticNet.prototype.faces = {
    sides: [],
    triangles: [],
    circles: [],
    edges: [],
    hexagons: []
}
SemanticNet.prototype.controls = {
    name: '',
    desc: '',
    show3: true,
    showv: true,
    showh: true,
    showe: true
}
SemanticNet.prototype.on100Click = function() {
    this.camera.position.z = 100;
}
SemanticNet.prototype.onPlusClick = function() {
    this.camera.position.z -= 100;
}
SemanticNet.prototype.onMinusClick = function() {
    this.camera.position.z += 100;
}
SemanticNet.prototype.addGuiControls = function() {
    if(window.dat && dat.hasOwnProperty('GUI')) {
        var gui = new dat.GUI({autoPlace: false});
        var f1 = gui.addFolder('Вершина');
        f1.add(this.controls, 'name').name('Название');
        f1.add(this.controls, 'desc').name('Описание');
        f1.open();

        var f2 = gui.addFolder('Controls');
        f2.add(this.controls, 'show3').name('Треугольники').onChange(this._trianglesToggle.bind(this));
        f2.add(this.controls, 'showv').name('Вершины').onChange(this._verticesToggle.bind(this));
        f2.add(this.controls, 'showh').name('Шестигранники').onChange(this._hexahedronToggle.bind(this));
        f2.add(this.controls, 'showe').name('Ребра').onChange(this._edgesToggle.bind(this));
        f2.open();

        $(gui.domElement).css({
            position: 'absolute',
            right: 0,
            bottom: 0
        }).appendTo(this.renderTo);

        this.gui = gui;
    }
}
SemanticNet.prototype.updateGui = function() {
    /*for (var i in this.gui.__controllers) {
        console.log(i, this.gui.__controllers[i])
        this.gui.__controllers[i].updateDisplay();
    }*/
    if(this.gui) {
        for(var i in this.gui.__folders) {
            for(var n in this.gui.__folders[i].__controllers) {
                //console.log("\t", this.gui.__folders[i].__controllers[n])
                this.gui.__folders[i].__controllers[n].updateDisplay()
            }
        }
    }
}
SemanticNet.prototype._trianglesToggle = function(newValue) {
    $.each(this.faces.sides, function(n, side) {
        side.triangles.visible = newValue
    });
}
SemanticNet.prototype._verticesToggle = function(newValue) {
    $.each(this.faces.sides, function(n, side) {
        side.circles.visible = newValue
    });
}
SemanticNet.prototype._hexahedronToggle = function(newValue) {
    $.each(this.faces.sides, function(n, side) {
        side.hexagons.visible = newValue
    });
}
SemanticNet.prototype._edgesToggle = function(newValue) {
    $.each(this.faces.sides, function(n, side) {
        side.edges.visible = newValue
    });
}


SemanticNet.prototype.initObjects = function () {
    var w = this.OPTIONS.TRIANGLE_SIZE;
    var len = this.OPTIONS.PYRAMYD_SIZE;
    var fw = w * len;

    var d = Math.sqrt(Math.pow(w, 2) - Math.pow(w, 2) / 4);
    var wd = Math.sqrt(Math.pow(fw, 2) - Math.pow(fw, 2) / 4);
    var rotate_x = -0.3402154337922689;//simle magic
    //var rotate_x = -Math.sin(Utils.deg2rad(19.89));

    var side;
    side = this.faces.sides[0] = new Semantic_net_Side(0, this, w, d, len);
    side.group.rotateY(Math.PI / 3);
    side.group.rotateX(rotate_x);

    side = this.faces.sides[1] = new Semantic_net_Side(1, this, w, d, len);
    side.group.position.x = -fw / 2;
    side.group.position.z = -wd;
    side.group.rotateY(5 * Math.PI / 3);
    side.group.rotateX(rotate_x);

    side = this.faces.sides[2] = new Semantic_net_Side(2, this, w, d, len, true);
    side.group.position.x = fw / 2;
    side.group.position.z = -wd;
    side.group.rotateY(Math.PI);
    side.group.rotateX(rotate_x);

    side = this.faces.sides[3] = new Semantic_net_Side(3, this, w, d, len);
    side.group.rotateX(-Math.PI / 2);
    side.group.rotateY(-Math.PI);
    side.group.rotateZ(Math.PI / 3);

    var pyramid = new THREE.Object3D();
    pyramid.add(this.faces.sides[0].group, this.faces.sides[1].group, this.faces.sides[2].group, this.faces.sides[3].group);
    pyramid.position.z = 2 * wd / 3;//move pyramid to center

    this.scene.updateMatrixWorld();
    this.scene.add(pyramid)
}

SemanticNet.prototype.animate = function () {
    requestAnimationFrame(this.animate.bind(this));
    this.render();
    this.update();
}

SemanticNet.prototype.update = function () {
    this.vcontrols.update();
    this.stats && this.stats.update();
}

SemanticNet.prototype.render = function () {
    this.renderer.render(this.scene, this.camera);
}