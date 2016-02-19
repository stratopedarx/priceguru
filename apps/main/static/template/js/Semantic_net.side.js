var Semantic_net_Side = function (face, parent, w, d, len, addtop) {
    //console.log('new Semantic_net_Side', arguments, parent)
    this.parent = parent;
    this.len = len;
    this.data = parent.data;

    this.hexagons = new THREE.Object3D();
    this.circles = new THREE.Object3D();
    this.triangles = new THREE.Object3D();
    this.edges = new THREE.Object3D();

    var group = new THREE.Object3D(),
        text_group = new THREE.Object3D(),
        geom = this.createTriangleGeometry(w, d);

    var shader = {
        'outline': {
            vertex_shader: [
                "uniform float offset;",
                "void main() {",
                "vec4 pos = modelViewMatrix * vec4( position + normal * offset, 1.0 );",
                "gl_Position = projectionMatrix * pos;",
                "}"].join("\n"),
            fragment_shader: [
                "void main(){",
                "gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );",
                "}"
            ].join("\n")
        }
    };

    for (var y = 0; y < len; y += 1) {
        var counter = 0;

        for (var x = 0; x < len - y; x += 1) {
            var pos = {
                x: w * x + y * w / 2,
                y: d * y
            };

            //нормальный треугольник
            counter += 1;

            var tr = this.createTriangle(geom, pos.x, pos.y, this.getColor(face, y, x));
            this.parent.events.setOnClick(tr, this.onTriangleClick);
            this.triangles.add(tr);
            //-----------------------------------
            //console.info('pos', pos)
            /*var line = this.addEdges(tr, pos, w, d);
            this.edges.add(line);*/

            var geometry = new THREE.Geometry();
            geometry.vertices = [
                new THREE.Vector3(-w / 2, 0, 0),
                new THREE.Vector3(0, d, 0),
                new THREE.Vector3(w / 2, 0, 0),
                new THREE.Vector3(-w / 2, 0, 0)
            ];
            
            
            // var material = new THREE.LineBasicMaterial({ color: '#000000' });

            // var line = new THREE.Line(geometry, material);
            // line.position.x = pos.x + w / 2;
            // line.position.y = pos.y;
            // this.edges.add(line);
            
            var materialForEdges = new THREE.LineBasicMaterial({ color: '#32374E'});
            var edgeRadius = 0.6;
            
            //left edge
            var numPoints = 3;
            var start = new THREE.Vector3(-w / 2, 0, 0);
            var middle = new THREE.Vector3(-w / 4, d / 2, 0);
            var end = new THREE.Vector3(0, d, 0);
            var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
            var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
            var mesh = new THREE.Mesh(tube, materialForEdges);
            mesh.position.x = pos.x + w / 2;
            mesh.position.y = pos.y;
            this.edges.add(mesh);
            
            
            //left edge text
            var edgeText = this.createEdgeText("placeholder", {
                size: 2,
                height: 0.1,
                curveSegments: 4,
                font: 'arial',
                style: 'normal',

                bevelThickness: 2,
                bevelSize: 1.5,
                bevelEnabled: false,

                material: 0,
                extrudeMaterial: 1,
            });

            var rotation = 60 * Math.PI / 180;
            var edgeBox = new THREE.Box3().setFromObject(edgeText);
            edgeText.position.x = pos.x + 4;
            edgeText.position.y = pos.y + 6;
            edgeText.position.z = 0.6;
            edgeText.rotateZ(rotation);
            text_group.add(edgeText);
            
            
            //right edge
            var numPoints = 3;
            var start = new THREE.Vector3(0, d, 0);
            var middle = new THREE.Vector3(w / 4, d / 2, 0);
            var end = new THREE.Vector3(w / 2, 0, 0);
            var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
            var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 20, false);
            var mesh = new THREE.Mesh(tube, materialForEdges);
            mesh.position.x = pos.x + w / 2;
            mesh.position.y = pos.y;
            this.edges.add(mesh);
            
            //right edge text
            var edgeText = this.createEdgeText("placeholder", {
                size: 2,
                height: 0.1,
                curveSegments: 4,
                font: 'arial',
                style: 'normal',

                bevelThickness: 2,
                bevelSize: 1.5,
                bevelEnabled: false,

                material: 0,
                extrudeMaterial: 1,
            });

            var rotation = -60 * Math.PI / 180;
            var edgeBox = new THREE.Box3().setFromObject(edgeText);
            edgeText.position.x = pos.x + d - 8;
            edgeText.position.y = pos.y + d - 7;
            edgeText.position.z = 0.6;
            edgeText.rotateZ(rotation);
            text_group.add(edgeText);
            
            
        
            
            
            
            //bottom edge
            var numPoints = 3;
            var start = new THREE.Vector3(w / 2, 0, 0);
            var middle = new THREE.Vector3(0, 0, 0);
            var end = new THREE.Vector3(-w / 2, 0, 0);
            var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
            var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 20, false);
            var mesh = new THREE.Mesh(tube, materialForEdges);
            mesh.position.x = pos.x + w / 2;
            mesh.position.y = pos.y;
            this.edges.add(mesh);
            
            //bottom edge text
            var edgeText = this.createEdgeText("placeholder", {
                size: 2,
                height: 0.1,
                curveSegments: 4,
                font: 'arial',
                style: 'normal',

                bevelThickness: 2,
                bevelSize: 1.5,
                bevelEnabled: false,

                material: 0,
                extrudeMaterial: 1,
            });

            var edgeBox = new THREE.Box3().setFromObject(edgeText);
            edgeText.position.x = pos.x - edgeBox.size().x / 2 + w / 2;
            edgeText.position.y = pos.y - 1;
            edgeText.position.z = 0.6;
            text_group.add(edgeText);



            if (x + 1 < len - y) {
                //перевернутый
                counter += 1;

                var rev = {
                    x: w * (x + 1) + (y + 1) * w / 2,
                    y: d * (y + 1)
                };

                var tr = this.createTriangle(geom, rev.x, rev.y, this.getColor(face, y, x, true));
                tr.rotation.z = Math.PI;

                this.parent.events.setOnClick(tr, this.onTriangleClick);
                //this.parent.events.setOnHover(tr, this.onTriangleHover, this.onTriangleUnHover);
                this.triangles.add(tr);


                // var line = new THREE.Line(geom, material);
                // line.position.x = rev.x + w / 2;
                // line.position.y = rev.y;
                // this.edges.add(line);


                this.triangles.add(tr);
            }

            var circle;
            if (x <= len - y + 1) {
                if (x == 0 && y == 0)
                    circle = this.createCircle(pos.x, pos.y, 0, this.BIG_CIRCLE_SIZE, this._colors.yellow);
                else if (x == 1 && y == 1 || x == 3 && y == 1 || x == 1 && y == 3)
                    circle = this.createCircle(pos.x, pos.y, 0, this.MID_CIRCLE_SIZE, this._colors.white);
                else
                    circle = this.createCircle(pos.x, pos.y, 0, this.SMALL_CIRCLE_SIZE, this._colors.white);

                var edge = null;
            }

            this.parent.events.setOnClick(circle, this.onCircleClick.bind(this));
            this.circles.add(circle);

            var t = this.data.pop().name
            var text = this.createText(t, {
                size: 2,
                height: 0.1,
                curveSegments: 4,
                font: 'arial',
                style: 'normal',

                bevelThickness: 2,
                bevelSize: 1.5,
                bevelEnabled: false,

                material: 0,
                extrudeMaterial: 1
            });

            //set center pos
            var box = new THREE.Box3().setFromObject(text);
            text.position.x = pos.x - box.size().x / 2 + w / 2;
            text.position.y = pos.y + 2;
            text_group.add(text);
        }
    }
    group.add(text_group);

    if (addtop) {
        //add top circle
        var circle = this.createCircle(
            geom.vertices[2].x + w / 2 * 4,
            geom.vertices[2].y + d * 4,
            geom.vertices[2].z,
            this.BIG_CIRCLE_SIZE,
            this._colors.yellow
            );
        this.parent.events.setOnClick(circle, this.onCircleClick.bind(this));
        this.circles.add(circle);
    }

    group.add(this.triangles);
    group.add(this.circles);
    group.add(this.edges);

    this.addHexagons(this.hexagons, w, d)
    group.add(this.hexagons);

    this.group = group;
};

Semantic_net_Side.prototype._colors = {
    Orange: '#FF9C00', Orange2: '#FFDEAD',
    Purple: '#D600D6', Purple2: '#FFCEFF',
    Green: '#84B500', Green2: '#F7FFBD',
    Blue: '#006bd6', Blue2: '#D6E7FF',
    yellow: '#FFFF00',
    black: '0x000000',
    neutral: '#FFFFC6'
}
Semantic_net_Side.prototype.getColor = function (face, y, x, rev) {
    var size = this.parent.OPTIONS.PYRAMYD_SIZE;

    if (rev) {
        if (y == 0) {
            if (x == 0 || x == 3)
                return this._colors.Orange2;
            else
                return this._colors.Green2;
        }
        else if (y == 1 && x == 1)
            return this._colors.Blue;
        else if (y == 1 || y == 2)
            return [this._colors.Green2, this._colors.Purple2, this._colors.Green2, this._colors.Purple2][face]
        else if (y == 3)
            return this._colors.Orange2;
    } else {
        if (y == 0) {
            if (x == 0 || x == size - 1)
                return this._colors.Orange;
            else if (x == 1 || x == 3)
                return this._colors.neutral;
            else if (x == 2)
                return [
                    this._colors.Purple, this._colors.Green, this._colors.Purple
                    /*,this._colors.Purple, this._colors.Green*/
                ][face]
        } else if (y == 1) {
            if (x == 0 || x == size - 2)
                return this._colors.neutral;
            else
                return this._colors.Blue2;
        } else if (y == 2) {
            return [
                [this._colors.Green, this._colors.Purple, this._colors.Green][x],
                this._colors.Blue2,
                [this._colors.Purple, this._colors.Green, this._colors.Purple][x]
            ][face];
            /*if (x == 0)
             return this._colors.Green;
             else if (x == 1)
             return this._colors.Blue2;
             else if (x == 2)
             return this._colors.Purple*/
        } else if (y == 3) {
            return this._colors.neutral;
        } else if (y == 4) {
            return this._colors.Orange;
        }
    }
};


/*
 #FF9C00 - orange - #FFDEAD
 #84B500 - green - #F7FFBD
 #0063CE - blue - #D6E7FF
 #D600D6 - purple - #FFCEFF
 */

Semantic_net_Side.prototype.BIG_CIRCLE_SIZE = 8;
Semantic_net_Side.prototype.MID_CIRCLE_SIZE = 6;
Semantic_net_Side.prototype.SMALL_CIRCLE_SIZE = 4;

Semantic_net_Side.prototype.addHexagons = function (group, w, d) {
    var alpha = w * Math.sqrt(3) / 6;
    var geometry = new THREE.Geometry();
    //hexahedron coordinates
    geometry.vertices = [
        new THREE.Vector3(w, d - alpha, 0),
        new THREE.Vector3(w, d + alpha, 0),
        new THREE.Vector3(w * 1.5, 2 * d - alpha, 0),
        new THREE.Vector3(w * 2, d + alpha, 0),
        new THREE.Vector3(w * 2, d - alpha, 0),
        new THREE.Vector3(w * 1.5, alpha, 0),
        new THREE.Vector3(w, d - alpha, 0)
    ];
    
    
    /*
    x - coordinate
    y - coordinate
    */
    function createHexagon(x, y) {

        var materialForEdges = new THREE.LineBasicMaterial({ color: '#ffffff',  transparent: true, opacity: 0.6 });
        var edgeRadius = 0.6;

        var numPoints = 3;
        var start = geometry.vertices[0];
        var middle = geometry.vertices[0];
        var end = geometry.vertices[1];
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);

        var start = new THREE.Vector3(w, d + alpha, 0);
        var middle = new THREE.Vector3(w, d + alpha, 0);
        var end = new THREE.Vector3(w * 1.5, 2 * d - alpha, 0);
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);

        var start = new THREE.Vector3(w * 1.5, 2 * d - alpha, 0);
        var middle = new THREE.Vector3(w * 1.5, 2 * d - alpha, 0);
        var end = new THREE.Vector3(w * 2, d + alpha, 0);
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);

        var start = new THREE.Vector3(w * 2, d + alpha, 0);
        var middle = new THREE.Vector3(w * 2, d + alpha, 0);
        var end = new THREE.Vector3(w * 2, d - alpha, 0);
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);

        var start = new THREE.Vector3(w * 2, d - alpha, 0);
        var middle = new THREE.Vector3(w * 2, d - alpha, 0);
        var end = new THREE.Vector3(w * 1.5, alpha, 0);
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);

        var start = new THREE.Vector3(w * 1.5, alpha, 0);
        var middle = new THREE.Vector3(w * 1.5, alpha, 0);
        var end = new THREE.Vector3(w, d - alpha, 0);
        var curve = new THREE.QuadraticBezierCurve3(start, middle, end);
        var tube = new THREE.TubeGeometry(curve, numPoints, edgeRadius, 8, false);
        var mesh = new THREE.Mesh(tube, materialForEdges);
        mesh.position.z = 1.6;
        mesh.position.x = x;
        mesh.position.y = y;
        group.add(mesh);
    }
            
    //bottom floor
    createHexagon(0, 0);
    createHexagon(w, 0);
    createHexagon(2 * w, 0);
            
            
    //middle floor
    createHexagon(w / 2, d);
    createHexagon(3 * w / 2, d);
            
    //top floor
    createHexagon(w, 2 * d);
};

Semantic_net_Side.prototype.onTriangleClick = function () {
    //console.log(this, this.material, arguments, Utils.getRandomColor());

    //this.material.color.setHex(Utils.getRandomColor())
    //console.log('this.material', this.material, this.material instanceof THREE.MeshBasicMaterial)
};
Semantic_net_Side.prototype.onTriangleHover = function () {
    console.log('onTriangleHover')
    this.prevColor = this.material.color
    this.material.color.setHex('#' + Utils.getRandomColor())
};
Semantic_net_Side.prototype.onTriangleUnHover = function () {
    console.log('onTriangleUnHover')

    //console.log(this.material.color)
    //this.prevColor = this.material.color
    this.material.color.setHex(this.prevColor)
};
Semantic_net_Side.prototype.onCircleClick = function () {
    //console.log('onCircleClick', this.parent.controls, this.parent.gui.__controllers)

    //this.material.color.setHex(Utils.getRandomColor())
    this.parent.controls.name = Date.now()
    this.parent.controls.desc = (new Date).getMilliseconds()

    this.parent.updateGui()
};


Semantic_net_Side.prototype.createTriangleGeometry = function (w, d) {
    var geom = new THREE.Geometry();

    geom.vertices.push(new THREE.Vector3(0, 0, 0));
    geom.vertices.push(new THREE.Vector3(w, 0, 0));
    geom.vertices.push(new THREE.Vector3(w / 2, d, 0));

    geom.faces.push(new THREE.Face3(0, 1, 2));
    //geom.computeFaceNormals();
    return geom;
};

Semantic_net_Side.prototype.createTriangle = function (geom, x, y, color) {
    //console.log('color', color)
    var mesh = new THREE.Mesh(geom, new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide }));
    mesh.position.x = x;
    mesh.position.y = y;

    return mesh
};
Semantic_net_Side.prototype.createCircle = function (x, y, z, size, color) {
    var mesh = new THREE.Mesh(
        new THREE.SphereGeometry(size),
        new THREE.MeshBasicMaterial({ color: color })
        );
    mesh.position.set(x, y, z);

    return mesh
};
Semantic_net_Side.prototype.createText = function (text, params) {
    return new THREE.Mesh(
        new THREE.TextGeometry(text, params),
        new THREE.MeshBasicMaterial({ color: '#000000' })
        )
};

Semantic_net_Side.prototype.createEdgeText = function (text, params) {
    return new THREE.Mesh(
        new THREE.TextGeometry(text, params),
        new THREE.MeshBasicMaterial({ color: '#FF0000' })
        )
};