'use strict';

define( function (){

    var Renderer = function (canvas) {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 10000 );
        this.camera.position.z = 1000;
        this.scene.add( this.camera );

        this.renderer = new THREE.WebGLRenderer({canvas:canvas[0]});
        this.renderer.setSize( 800, 640 );
        this.continiousRender = false;

        this.startRendering();

    };

    Renderer.prototype.startRendering = function () {
        this.continiousRender = true;
        this.render();
    };

    Renderer.prototype.render = function () {
        this.renderer.render(this.scene, this.camera);
        if (this.continiousRender) {
            webkitRequestAnimationFrame(this.render.bind(this));
        }
    };

    return Renderer;
});
