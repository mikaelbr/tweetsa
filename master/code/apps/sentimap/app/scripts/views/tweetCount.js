define(['backbone', 'vent'], function(Backbone, vent) {
   
  return Backbone.View.extend({
    el: '#total-tweet-count',

    initialize: function (options) {
      this.model.on('change', this.render, this);
      vent.on('map:reset', this.reset, this);
      vent.on('stats:increase_count', this.increase, this);
    },

    reset: function () {
      this.model.set('count', 0);
    },

    increase: function () {
      this.model.increase();
    },

    render: function () {
      this.$el.text(this.model.get('count'));
    }

  });
    
});