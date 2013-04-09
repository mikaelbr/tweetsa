define(['backbone', 'jquery', 'vent', 'views/streamBase'], function(Backbone, $, vent, StreamBase) {
 
  var SearchStream = StreamBase.extend({
    title: 'Showing real time tweets for «{{query}}»:',

    render: function (query) {
      var that = this;
      this.resetViews();

      this.$titleEl.html(this.title.replace('{{query}}', $("<div/>").html(query).html()));

      this.searchSocket = io.connect(this.wsBase + this.searchChannel);
      this.searchSocket.on('tweet', $.proxy(this.handleWebSocket, this));
      this.searchSocket.emit('search', query, function () {
        vent.trigger('map:reset');
        that.collection.resetStates();
      });
      return this;
    }
  });

  return SearchStream;
});