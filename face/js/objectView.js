'use strict';

define(function () {
    var ObjectView = function (options) {
        this.manager = options.manager;
        this.frame = new THREE.Mesh(new THREE.CubeGeometry(100, 100, 1),
            new THREE.MeshLambertMaterial({
                color:0xffaa88
            }));

        this.base = new THREE.Mesh(new THREE.CubeGeometry(95, 95, 3),
            new THREE.MeshLambertMaterial({
                color:0xcccccc
            }));
        this.frame.add(this.base);

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
