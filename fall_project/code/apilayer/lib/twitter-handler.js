var util     = require('util')
  , events   = require('events')
  , Twitter  = require('ntwitter')
  , config   = require('config').Twitter
  , sentiment = require('./sentiment-provider')
  , async     = require('async');


// Constructor
var TwitterHandler = function () {
  if(false === (this instanceof TwitterHandler)) {
    return new TwitterHandler();
  }

  // Use emitter or not? Maybe emitting isn't the best solution for this.
  // events.EventEmitter.call(this);
  this.init();
};

// util.inherits(TwitterHandler, events.EventEmitter);

// Private functions
var constructErrorJSON = function (msg, code) {
  code = code || 400;
  msg = msg || "Unknown error";

  return {
    "errors": [
      {
        "code": code,
        "message": msg
      }
    ]
  };
};

var generateParamList = function (req, params) {
  var keys = Object.keys(params)
    , results = {};

  // blocking foreach, safe to use as sync
  keys.forEach(function (item) {
    var isRequired = !!params[item]
      , paramValue = req.param(item);

    if ( typeof paramValue === "undefined") {

      if (isRequired) {
        throw constructErrorJSON("Required field not given", 400);
      }

    } else {
      results[item] = paramValue;
    }
  });

  return results;
};


var constructSentimentJSON = function (sentimentString) {
  return {
    classification: sentimentString.toString().trim()
  };
};

var iterator = function (item, callback) {
  var start = +new Date();

  sentiment.get(item).on("data", function (classification) {
    item.sentiment = constructSentimentJSON(classification);
    var end = +new Date();
    console.log("A spesific classification done in " + (end-start)/1000 + " seconds");
    callback(null, item);
  });
};

// Prototype methods
TwitterHandler.prototype.init = function () {
  // Do some initialization.
  this.twit = new Twitter({
    consumer_key:  config.consumer_key,
    consumer_secret:  config.consumer_secret,
    access_token_key:  config.access_token_key,
    access_token_secret: config.access_token_secret
  });

};

// etc...
TwitterHandler.prototype.search = function (req, cb) {
  var paramList = {
    q: true,
    geocode: false,
    lang: false,
    locale: false,
    result_type: false,
    count: false,
    until: false,
    since_id: false,
    max_id: false,
    include_entities: false,
    callback: false
  };

  try {
    var rp = generateParamList(req, paramList);

    var ostart = +new Date();
    this.twit.get("/search/tweets.json", rp, function(err, data) {
      if (err) throw err;
      var oend = +new Date();

      console.log("Twitter search done in " + (oend-ostart)/1000 + " seconds");

      var start = +new Date();
      async.map(data.statuses, iterator, function (err, results) {
        var end = +new Date();
        console.log("Entire classification done in " + (end-start)/1000 + " seconds");
        cb(null, data);
      });
    });
  } catch (e) {
    cb(e);
  }

  return this;
};


TwitterHandler.prototype.statusesFilter = function (req, cb) {
  var paramList = {
    follow: false,
    track: false,
    locations: false,
    delimited: false,
    stall_warnings: false
  };

  var eventEmitter = new events.EventEmitter();

  var rp = generateParamList(req, paramList);

  if (!rp.track && !rp.locations && !rp.follow) {
    throw constructErrorJSON("No filter parameters found. Expect at least one parameter: follow track locations", 406);
  } 

  this.twit.stream('statuses/filter', rp, function(stream) {
    stream.on('data', function (data) {
      sentiment.get(data).on("data", function (classification) {
        data.sentiment = constructSentimentJSON(classification);
        eventEmitter.emit('data', data);
      });
    });
    stream.on('error', function (err, errorCode) {
      eventEmitter.emit('error', constructErrorJSON(err, errorCode));
    });
    stream.on('end', function (response) {
      // Handle a disconnection
      eventEmitter.emit('end', response);
    });
  });

  return eventEmitter;

};


module.exports = new TwitterHandler();
