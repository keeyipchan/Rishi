'use strict';

define(['sceneManager', 'objectModel', 'objectCollection', 'app'], function (SceneManager, ObjectModel, ObjectCollection, App){
    var sceneManager = new SceneManager($('#viewport'));
    var app = new App({
        sceneManager: sceneManager
    });

    Backbone.sync = function (method, model, options) {
        console.log('sync:',method,model,options);
    };

    app.objects.add(new ObjectModel());

//    sceneManager.render();
});
