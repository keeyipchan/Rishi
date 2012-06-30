'use strict';

define(['sceneManager', 'objectModel', 'objectCollection', 'app', 'connection'], function (SceneManager, ObjectModel, ObjectCollection, App, Connection){
    var sceneManager = new SceneManager($('#viewport'));
    var connection = new Connection('http://localhost:8000/data');
    var app = new App({
        sceneManager: sceneManager,
        connection: connection
    });

    Backbone.sync = function (method, model, options) {
        console.log('sync:',method,model,options);
    };

    app.start();


//    sceneManager.render();
});
