'use strict';

/**
 * Model of language object
 * properties:
 *  name
 *  fields
 *  type
 *  links
 */

define( function (){
    var ObjectModel = Backbone.Model.extend({
        defaults: function () {
            return {
                name:'<NoName>',
                fields: [],
                type: 'generic',
                links: []
            }
        }
    });

    return ObjectModel;
});
