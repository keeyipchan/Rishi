'use strict';

define(['renderer', 'objectModel', 'objectCollection', 'app'], function (Renderer, ObjectModel, ObjectCollection, App){
    var renderer = new Renderer($('#viewport'));
    var app = new App({
        scene: renderer.scene
    });

    Backbone.sync = function (method, model, options) {
        console.log('sync:',method,model,options);
    };

    app.objects.add(new ObjectModel());

    renderer.render();
});
