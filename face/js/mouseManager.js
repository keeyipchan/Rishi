'use strict';


define(function () {
    var MouseManager = function (node) {
        this.node = $(node);
        this._bindEvents();
    };

    MouseManager.prototype = {
        _bindEvents:function () {
            this.node.on('mousedown', this._mouseDown.bind(this));
            this.node.on('mousemove', this._mouseMove.bind(this));
            this.node.on('mouseup', this._mouseUp.bind(this));
            this.node.on('mousewheel', this._mouseWheel.bind(this));
        },
        _mouseDown:function (e) {
            this.dragging = true;
            this.pageX = e.pageX;
            this.pageY = e.pageY;
        },
        _mouseMove:function (e) {
            if (!this.dragging) return;
            this.trigger('drag', e.pageX - this.pageX, e.pageY - this.pageY, e.which);
            this.pageX = e.pageX;
            this.pageY = e.pageY;
        },
        _mouseUp:function (e) {
            this.dragging = false;
        },
        _mouseWheel:function (e) {
            var delta = e.originalEvent.wheelDelta;
            delta = delta > 0 ? 1
                : delta < 0 ?
                -1 : 0;
            this.trigger('zoom', delta)
        }

    };

    _.extend(MouseManager.prototype, Backbone.Events);

    return MouseManager;
});
