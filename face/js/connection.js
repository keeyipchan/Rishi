'use strict';


define(function () {
    var Connection = function (url) {
        if (url && url[url.length - 1] !== '/') url += '/';
        this.url = url || '';
    };

    Connection.prototype = {
        getJSON:function (path, params, callback) {
            return $.getJSON(this.url + path, params, function (data, testStatus, jqXHR) {
                if (callback) callback(data);
            })
        },
        loadObjectTree:function () {
            this.getJSON('ObjectTree.json').success(function (data) {
                console.log(data);
                this.trigger('objectTreeLoaded', data);
            }.bind(this)).error(function () {
                    console.log('error loading object tree')
                });
        }
    };

    _.extend(Connection.prototype, Backbone.Events);

    return Connection;
});
