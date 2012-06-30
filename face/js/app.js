'use strict';

define(['objectCollection', 'objectView'], function (ObjectCollection, ObjectView) {
    var App = function (options) {
        this.sceneManager = options.sceneManager;
        this.objects = new ObjectCollection();
        this.objects.on('add', this.onObjectAdd.bind(this));
        this.objectViews = [];
        this.connection = options.connection;
        this.connection.on('objectTreeLoaded', this.onObjectTreeLoaded.bind(this))
    };

    App.prototype = {
        start : function () {
            this.connection.loadObjectTree();
        },
        onObjectAdd:function (object) {
            var view = new ObjectView({model:object, manager:this.sceneManager});
            this.objectViews.push(view);
        },
        onObjectTreeLoaded:function (tree) {
            console.log('tree!!')
        }
    };


    return App;
});
