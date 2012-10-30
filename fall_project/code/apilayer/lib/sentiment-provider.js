/** 
 * Sentiment Provider.
 * Using an external CLI to find sentiment by given tweet. 
 */

var CONFIG = require('config');


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

  if (!_is_string(tweet)) {
    tweet = JSON.stringify(tweet);
  }

  // Get sentiment
  var spawn = require('child_process').spawn;
  return spawn('python', [CONFIG.Sentiment.cliPath, tweet]).stdout;
}


module.exports = new SentimentAnalysis();