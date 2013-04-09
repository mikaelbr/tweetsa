
/**
 * Module dependencies.
 */

var express = require('express')
  , http = require('http')
  , path = require('path')
  , twitter = require('sntwitter')
  , utils = require('./utils')
  , CONFIG = require('config').Map

var app = express();


var twit = new twitter();

// all environments
app.set('port', process.env.PORT || 5001);
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'app')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

var server = http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});

var io = require('socket.io').listen(server,  { log: false })
  , connectCounter = 0;

var streamHandler = function (sockEmitter, stream, query) {
  stream.on('data', function (data) {
    if (!data || !data.place || !data.place.country_code || data.place.country_code !== "US") {
      return;
    }

    if (data.sentiment.classification === "neutral") {
      return;
    }

    var stateArr = data.place.full_name.split(", ")
      , state = stateArr[stateArr.length - 1];

    // Check if the full name is a state. 
    if (state === "US") {
      // is state. convert
      state = utils.generateStateCode(stateArr[0]);
    }

    if (!state) {
      return;
    }

    if (query && data.text.toLowerCase().indexOf(query.toLowerCase()) === -1) {
      // Filter by query...
      return;
    }

    data.state = state;
    sockEmitter.emit('tweet', data);  
  });
};

var twee = io
  .of('/tweet')
  .on('connection', function (socket) {
    var twitStream = null;
    connectCounter++;

    if (connectCounter === 1) {
      // Iniit stream
      twit.stream('statuses/filter', {'locations': CONFIG.US_BoundingBox}, function (stream) {
        twitStream = stream;
        streamHandler(twee, stream);
      });
    }

    socket.on('disconnect', function() { 
      connectCounter--; 

      if (connectCounter <= 0) {
        // Destroy stream
        twitStream && twitStream.destroy();
      }
    });
});

var search = io
  .of('/search')
  .on('connection', function (socket) {
    var twitStream = null;

    socket.on('search', function (query) {
      twit.stream('statuses/filter', {'locations': CONFIG.US_BoundingBox}, function (stream) {
        twitStream = stream;
        streamHandler(socket, stream, query);
      });
    });

    socket.on('disconnect', function() { 
        // Destroy stream
        twitStream && twitStream.destroy();
    });
});

