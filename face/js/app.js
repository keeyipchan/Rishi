'use strict';

define(['objectModel','objectCollection', 'objectView'], function (ObjectModel,ObjectCollection, ObjectView) {
    var App = function (options) {
        this.sceneManager = options.sceneManager;
        this.objects = new ObjectCollection();
        this.objects.on('add', this.onObjectAdd.bind(this));

        this.objectViews = [];
        this.connection = options.connection;
        this.connection.on('objectTreeLoaded', this.onObjectTreeLoaded.bind(this))
        this.classes = [];
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
            var flat = flattenTree(tree);

            for (var i=0;i<flat.length;i++) {
                if (flat[i].type == 'class')  {
                    this.classes.push(flat[i]);
                    this.objects.add(new ObjectModel(flat[i]))
                }
            }

        }
    };

    //convert JSON tree to array of linked object models
    function flattenTree(root, parent) {
        var res = [];
        root.parent = parent || null;
        res.push(root);
        for (var f in root.fields) {
            var flat = flattenTree(root.fields[f], root);
            root.fields[f] = flat[0];
            res = res.concat(flat);
        }
        return res;
    }

    return App;
});
