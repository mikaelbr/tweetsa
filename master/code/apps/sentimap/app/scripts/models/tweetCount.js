define(['backbone', 'jquery'], function(Backbone, $) {
   
    var TweetCount = Backbone.Model.extend({

      defaults: {
        count: 0
      },

      increase: function () {
        this.set({
          count: this.get('count') + 1,
        });
        return this;
      },

    });
   
    return TweetCount; 
});