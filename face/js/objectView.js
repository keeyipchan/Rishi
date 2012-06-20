'use strict';

define( function (){
    var ObjectView = Backbone.View.extend({
        initialize: function () {
            //
            this.scene = this.options.scene;
            this.geometry = new THREE.Mesh( new THREE.CubeGeometry( 200, 200, 200 ), new THREE.MeshNormalMaterial() );
            this.geometry.position.y = 150;
            this.scene.add( this.geometry );
        },
        render : function () {
            console.log('render');
            return this;
        }
    });

    return ObjectView;
});
