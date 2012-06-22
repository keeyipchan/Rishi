'use strict';


define(function () {
    var MouseManager = function (node) {
        this.node = $(node);
        this._bindEvents();
    };

    MouseManager.prototype = {
        _bindEvents : function () {
            this.node.on('mousedown', this._mouseDown.bind(this))
            this.node.on('mousemove', this._mouseMove.bind(this))
            this.node.on('mouseup', this._mouseUp.bind(this))
        },
        _mouseDown : function (e) {
            this.dragging = true;
            this.pageX = e.pageX;
            this.pageY = e.pageY;
        },
        _mouseMove : function (e) {
            if (!this.dragging) return;
            this.trigger('drag', e.pageX - this.pageX, e.pageY - this.pageY, e.which);
            this.pageX = e.pageX;
            this.pageY = e.pageY;
        },
        _mouseUp : function (e) {
            this.dragging = false;
        }

    };

    _.extend(MouseManager.prototype, Backbone.Events);

    return MouseManager;
});
