define(
    ['backbone', 'jquery', 'views/map', 'vent', 'models/tweetCount', 'views/tweetCount', 'views/search', 'views/public', 'models/stats', 'views/timedStats', 'views/loading', 'views/background']
  , function(Backbone, $, Map, vent, TweetCount, TweetCountView, SearchStream, PublicStream, Stats, TimedStatsView, LoadingIndicator, BackgroundLoader) {
  
  var App = Backbone.View.extend({
    el: 'body',

    initialize: function() {
      var that = this;
      // this.loading = new LoadingIndicator();
      this.backgroundLoader = new BackgroundLoader().start();
     
      this.map = new Map();

      this.initCountStats();
      this.initStatsAccumulator();
      
      this.publicStream = new PublicStream({
        collection: this.map.collection
      }).render(); // render to start.

      this.searchStream = new SearchStream({
        collection: this.map.collection
      });

      this.loadElements();

    },

    events: {
      'submit form': 'setMode'
    },

    loadElements: function () {
      var $searchBox = this.$el.find('.search-form')
        , $map = this.$el.find('.map-container');

      $searchBox.animate({
        'top': '10px'
      }, 300, function () {
        setTimeout(function () {
          $map.fadeIn();
        }, 300);
      });
    },

    setMode: function (e) {
      e.preventDefault();
      var query = this.$el.find('#tweet-search').val();
      
      if (!query || !$.trim(query)) {
        return this.publicStream.render();
      }

      return this.searchStream.render(query);
    },

    initCountStats: function () {
      this.tweetCount = new TweetCount();
      new TweetCountView({
        model: this.tweetCount
      });
    },

    initStatsAccumulator: function () {
      this.timedStats = new TimedStatsView({
        model: new Stats()
      }).render();
    }

  });  

  return App;
});