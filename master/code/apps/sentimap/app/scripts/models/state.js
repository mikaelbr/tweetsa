define(['backbone', 'jquery'], function(Backbone, $) {
   
    var State = Backbone.Model.extend({

      defaults: {
        positive: 0,
        negative: 0,
        sentiment: 0,
      },

      positiveTweet: function () {
        this.set({
          sentiment: this.get('sentiment') + 1,
          positive: this.get('positive') + 1
        });
        return this;
      },

      negativeTweet: function () {
        this.set({
          sentiment: this.get('sentiment') - 1,
          negative: this.get('negative') + 1
        });
        return this;
      },

      toString: function () {
        return this.get('id') + ': ' + this.get('positive') + 'p, ' + this.get('negative') + 'n';
      }
    });
   
    return State; 
});