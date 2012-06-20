'use strict';

define(['objectCollection', 'objectView'], function (ObjectCollection, ObjectView){
    var App = function (options) {
        this.scene = options.scene;
        this.objects = new ObjectCollection();
        this.objects.on('add', this.onObjectAdd.bind(this));
        this.objectViews = [];
    };

    App.prototype.onObjectAdd = function (object) {
        var view = new ObjectView({model: object, scene: this.scene});
        this.objectViews.push(view);
        view.render();
    };

    return App;
});
