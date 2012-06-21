'use strict';

define(['objectCollection', 'objectView'], function (ObjectCollection, ObjectView){
    var App = function (options) {
        this.sceneManager = options.sceneManager;
        this.objects = new ObjectCollection();
        this.objects.on('add', this.onObjectAdd.bind(this));
        this.objectViews = [];
    };

    App.prototype.onObjectAdd = function (object) {
        var view = new ObjectView({model: object, manager: this.sceneManager});
        this.objectViews.push(view);
    };

    return App;
});
