'use strict';

define(['utils'], function (Utils) {
    var ObjectView = function (options) {
        this.manager = options.manager;
        this.model = options.model;


        this.frame = new THREE.Mesh(new THREE.CubeGeometry(100, 100, 1),
            new THREE.MeshLambertMaterial({
                color:0xffaa88
//                map:this.texture
            }));

        this.base = new THREE.Mesh(new THREE.CubeGeometry(95, 95, 3),
            new THREE.MeshLambertMaterial({
                color:0xcccccc

            }));
        this.base.position.z = 3 / 2;
        this.frame.add(this.base);

        var c = document.createElement('canvas');
        c.setAttribute('width', 95 * 3);
        c.setAttribute('height', 15 * 3);
        Utils.renderText(this.model.get('name'), c);

        this.titleTex = new THREE.Texture(c);
        this.titleTex.needsUpdate = true;
        var materials = [new THREE.MeshBasicMaterial({color:0xffffff})];
        materials[2] = materials[3] = materials[4] = materials[5] = materials[1] = materials[0];
        materials[4] = new THREE.MeshBasicMaterial({map:this.titleTex});

        var geo = new THREE.CubeGeometry(95, 15, 3, 1, 1, 1, materials);
        this.title = new THREE.Mesh(geo, new THREE.MeshFaceMaterial());

        this.title.position.z = 3;
        this.title.position.y = (95 - 15) / 2;
        this.base.add(this.title);

//            this.base.position.z = 10;
        this.manager.add(this);
    };

    ObjectView.prototype = {
        addToScene:function (scene) {
            scene.add(this.frame);
        }
    };

    return ObjectView;
});
