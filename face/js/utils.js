'use strict';

define(function(){
//    $('<div id="spawn_pool"></div>').css({overflow:'hidden', width:0, height:0}).appendTo('body');
    var Utils = {};

    Utils.renderText = function (text,canvas) {
        var context = canvas.getContext('2d');
        context.fillStyle = '#ffffff';
        context.fillRect(0, 0, canvas.width , canvas.height );
        context.fillStyle = 'black';
        context.font = '30px Arial';
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillText(text, canvas.width / 2, canvas.height / 2);

        return canvas;
    };

    return Utils;
});
