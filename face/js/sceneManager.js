'use strict';

define(['mouseManager'], function (MouseManager) {

    var SceneManager = function ($canvas) {
        this.$canvas = $canvas;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 10000);
        this.camera.position.z = 1000;
        this.scene.add(this.camera);

        this.blocks = [];
        this.ambLight = new THREE.AmbientLight( 0x101010 );
        this.scene.add( this.ambLight );

        this.mainLight = new THREE.DirectionalLight( 0xffffff );
        this.mainLight.position.set( 0, 0, 100 ).normalize()
        this.scene.add( this.mainLight );

        this.continiousRender = false;
        this.renderPending = false;

        this.renderer = new THREE.WebGLRenderer({canvas:$canvas[0]});
        this.renderer.setSize(window.innerWidth, window.innerHeight);

        var worldDot = new THREE.Mesh( new THREE.SphereGeometry( 10, 10, 10 ),
            new THREE.MeshLambertMaterial({
                color: 0x0000ff
            }) );

        this.scene.add(worldDot);

        this.mouseManager = new MouseManager(this.$canvas);
        this.mouseManager.on('drag', this.mouseDrag.bind(this));



        this.startRendering();
    };

    SceneManager.prototype = {
        mouseDrag: function (dx,dy) {
            this.moveCamera(dx,dy,0);
        },

        moveCamera: function (rx,ry,rz) {
            this.camera.position.x-=rx;
            this.camera.position.y+=ry;
        },

        startRendering:function () {
            this.continiousRender = true;
            this.render();
        },

        render:function () {
            this.renderPending = false;
            this.renderer.render(this.scene, this.camera);
            if (this.continiousRender && !this.renderPending) {
                this.renderPending = true;
                webkitRequestAnimationFrame(this.render.bind(this));
            }
        },
        add:function (block) {
            this.blocks.push(block);
            this.scene.add(block.geometry);
            this.reArrangeBlocks();
            this.render();
        },


        reArrangeBlocks:function () {
            for (var i = 0; i< this.blocks.length; i++) {
                this.blocks[i].geometry.position.set(i*120 + 50, 50, 0);
            }
        }
    };


    return SceneManager;
});
