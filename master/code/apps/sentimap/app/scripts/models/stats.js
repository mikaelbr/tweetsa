define(['backbone', 'jquery'], function(Backbone, $) {
   
    var State = Backbone.Model.extend({

      defaults: {
        data: []
      },

      pushData: function (pos, neg) {
        var arr = this.get('data');
        arr.push([ (new Date()).getTime(), (pos - neg) ]);
        this.set('data', arr);
        this.trigger("change");
        return this;
      }

    });
   
    return State; 
});