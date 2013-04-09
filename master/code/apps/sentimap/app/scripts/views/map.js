define(['backbone', 'underscore', 'jquery', 'collections/states', 'views/state', 'usmap'], function(Backbone, _, $, StatesCollection, StateView) {
   
  return Backbone.View.extend({
    el: '#map',

    defaultOptions: {
      showLabels: false, // don't show labels on map
      stateStyles: {fill: '#f5f5f5'},
      labelBackingStyles: {fill: '#f5f5f5'},
      labelTextStyles: {color: "black"},
      stateHoverStyles: { }, // deactivate hover effect.
      labelBackingHoverStyles: { } // deactivate hover effect.
    },

    initialize: function (options) {
      var that = this;
      this.usmap = (function () {
        return $.proxy(that.$el.usmap, that.$el);
      }());

      this.defaultOptions = _.extend({}, this.defaultOptions, options);
      this.render();

      this.collection = new StatesCollection(_.map(this.usmap('getStateNames'), function (obj) {
        return { 'id': obj };
      }));

      this.addAll();
    },

    render: function () {
      this.usmap(this.defaultOptions);
      return this;
    },

    addAll: function (collection) {
      this.collection.each(this.addOne, this);
    },

    addOne: function (stateModel) {
      new StateView({
        model: stateModel,
        stateData: this.usmap('getState', stateModel.get('id'))
      });
    }

  });
    
});