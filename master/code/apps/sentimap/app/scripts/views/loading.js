define(['backbone', 'underscore', 'jquery', 'vent'], function(Backbone, _, $, vent) {

    var Loading = Backbone.View.extend({
      el: '#loading',

      initialize: function () {
        var that = this;
        setTimeout(function () {
          that.$el.fadeOut();

        }, 500);
      },

      showLoading: function () {
        this.$el.show();
      },

      hideLoading: function () {
        this.$el.hide();
      }
    });
   
    return Loading; 
});

