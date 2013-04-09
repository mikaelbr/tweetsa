define(['backbone', 'jquery', 'vent', 'views/streamBase'], function(Backbone, $, vent, StreamBase) {
 
  var PublicStream = StreamBase.extend({
    title: 'Showing real time tweets from the USA',

    render: function () {
      this.$titleEl.html(this.title);

      this.resetViews();
      this.streamSocket = io.connect(this.wsBase + this.streamChannel);
      this.streamSocket.on('tweet', $.proxy(this.handleWebSocket, this));
      return this;
    }
  });

  return PublicStream;
});