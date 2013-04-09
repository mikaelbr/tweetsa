define(['backbone', 'models/state'], function(Backbone, State) {
   
    var States = Backbone.Collection.extend({
      model: State,

      resetStates: function () {
        this.each(function(model) {
          model.set({
            'sentiment': 0,
            'negative': 0,
            'positive': 0,
          });
        });
      }
    });
   
    return States; 
});
