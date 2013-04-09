define(['backbone', 'jquery', 'views/map', 'vent'], function(Backbone, $, Map, vent) {
 
  var StreamBase = Backbone.View.extend({
    el: 'body',
    "$titleEl": $('#site-title'),
    wsBase: (function () {
      if (!window.location.origin) {
        window.location.origin = window.location.protocol+"//" + window.location.host;
      }

      if (!window.location.origin) {
        return 'http://localhost:5001';
      }
      return window.location.origin;
      
    }()),
    streamChannel: '/tweet',
    searchChannel: '/search',

    handleWebSocket: function (data) {
      if (!data || !data.state) {
        return;
      }

      var state = data.state
        , sentiment = data.sentiment.classification;

      var stateModel = this.collection.get(state);
      if (!stateModel) {
        return;
      }

      vent.trigger('stats:increase_count');

      if (sentiment === "positive") {
        stateModel.positiveTweet();
        vent.trigger('tweet:positive');
      } else if (sentiment === "negative") {
        stateModel.negativeTweet();
        vent.trigger('tweet:negative');
      }
    },

    resetViews: function () {
      if(this.streamSocket || this.searchSocket) {
        this.streamSocket && this.streamSocket.disconnect();
        this.searchSocket && this.searchSocket.disconnect();

        io.sockets[this.wsBase].disconnect();
        delete io.sockets[this.wsBase]; 
        io.j =[];
      } 

      vent.trigger('map:reset');
      this.collection.resetStates();
    }
  });

  

  return StreamBase;
});