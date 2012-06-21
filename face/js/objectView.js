'use strict';

define( function (){
    var ObjectView = Backbone.View.extend({
        initialize: function () {
            //
            this.manager = this.options.manager;
            this.geometry = new THREE.Mesh( new THREE.CubeGeometry( 100, 100, 10 ),
                new THREE.MeshLambertMaterial({
                    color: 0xff0000
                }) );
//            this.geometry.position.y = 50;
            this.manager.add( this );
        },
        render : function () {
            console.log('render');
            return this;
        }
    });

    return ObjectView;
});
