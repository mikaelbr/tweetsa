/** 
 * Sentiment Provider.
 * Using an external CLI to find sentiment by given tweet. 
 */

var config = require('config')
  , http = require('http')
  , events   = require('events');


// Constructor
var SentimentAnalysis = function () {
    if(false === (this instanceof SentimentAnalysis)) {
      return new SentimentAnalysis();
    }
    // Do some initialization?
};

// Private functions?
var _is_string = function (input) {
  return typeof(input)=='string';
};




// Prototype methods.
SentimentAnalysis.prototype.get = function (tweet) {
  var eventEmitter = new events.EventEmitter();

  if (!_is_string(tweet)) {
    tweet = JSON.stringify(tweet);
  }

  var post_options = {
      host: config.Sentiment.server_host,
      port: config.Sentiment.server_port,
      method: 'POST'
  };

  // Set up the request
  var post_req = http.request(post_options, function(res) {
      var output = "";
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
          output += chunk;
      });

      res.on('end', function () {
          eventEmitter.emit('data', [output]);
      });
  });

  // post the data
  post_req.write(tweet);
  post_req.end();
  return eventEmitter;
};


module.exports = new SentimentAnalysis();