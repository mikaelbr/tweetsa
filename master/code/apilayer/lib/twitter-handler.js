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
        console.log(item);
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

var handleResponse = function(err, data, cb) {
  if (err) return cb(err);
  var start = +new Date();

  async.map(data, iterator, function (err, results) {
    var end = +new Date();
    console.log("Entire classification took " + (end-start)/1000 + " seconds");
    cb(null, data);
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
    include_entities: false
  };

  try {
    var rp = generateParamList(req, paramList);

    var start = +new Date();    
    this.twit.get("/search/tweets.json", rp, function(err, data) {
      var end = +new Date();
      console.log("Twitter search/lookup took " + (end-start)/1000 + " seconds");
      if (err) return handleResponse(err, null, cb);
      handleResponse(err, data.statuses, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;
};


TwitterHandler.prototype.retweets = function (req, cb) {
  var paramList = {
    id: true,
    count: false,
    trim_user: false
  };

  try {
    var rp = generateParamList(req, paramList);

    this.twit.get("/statuses/retweets/" + rp.id + ".json", rp, function(err, data) {
      handleResponse(err, data, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;
};


// etc...
TwitterHandler.prototype.show = function (req, cb) {
  var paramList = {
    id: true,
    include_my_retweet: false,
    include_entities: false,
    trim_user: false
  };

  try {
    var rp = generateParamList(req, paramList);

    this.twit.get("/statuses/show.json", rp, function(err, data) {
      iterator(data, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;
};


TwitterHandler.prototype.lists = function (req, cb) {

  var paramList = {
    list_id: false,
    slug: false,
    owner_screen_name: false,
    owner_id: false,
    since_id: false,
    max_id: false,
    count: false,
    include_entities: false,
    include_rts: false
  };

  try {
    var rp = generateParamList(req, paramList);

    if (!rp.list_id && !rp.slug) {
      cb(constructErrorJSON("No list parameter found. Expect at least one parameter: list_id slug", 406));
    }

    if (rp.slug && !rp.owner_screen_name && !rp.owner_id) {
      cb(constructErrorJSON("No list owner parameter found. Expect at least one parameter: owner_screen_name owner_id", 406));
    }

    this.twit.get("/lists/statuses.json", rp, function(err, data) {
      handleResponse(err, data, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;

};

TwitterHandler.prototype.listsShow = function (req, cb) {

  var paramList = {
    list_id: false,
    slug: false,
    owner_screen_name: false,
    owner_id: false
  };

  try {
    var rp = generateParamList(req, paramList);

    if (!rp.list_id && !rp.slug) {
      cb(constructErrorJSON("No list parameter found. Expect at least one parameter: list_id slug", 406));
    }

    if (rp.slug && !rp.owner_screen_name && !rp.owner_id) {
      cb(constructErrorJSON("No list owner parameter found. Expect at least one parameter: owner_screen_name owner_id", 406));
    }

    this.twit.get("/lists/show.json", rp, function(err, data) {
      handleResponse(err, data, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;

};



TwitterHandler.prototype.favorites = function (req, cb) {

  var paramList = {
    user_id: false,
    screen_name: false,
    count: false,
    since_id: false,
    max_id: false,
    include_entities: false
  };

  try {
    var rp = generateParamList(req, paramList);

    if (!rp.user_id && !rp.screen_name) {
      cb(constructErrorJSON("No user parameter found. Expect at least one parameter: user_id. screen_name", 406));
    } 

    this.twit.get("/favorites/list.json", rp, function(err, data) {
      handleResponse(err, data, cb);
    });
  } catch (e) {
    cb(e);
  }

  return this;

};

/****************************************************
 *                     STREAMING                    *
 ****************************************************/

var streamHelper = function (streamMethod, rp, eventEmitter) {
  this.twit.stream(streamMethod, rp, function(stream) {

    eventEmitter.destroy = function () {
      stream.destroy();
    };

    stream.on('data', function (data) {
      var start = +new Date(); 
      sentiment.get(data).on("data", function (classification) {
        var end = +new Date();
        console.log("Classification of stream item took " + (end-start)/1000 + " seconds");
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
};

TwitterHandler.prototype.statusesFilter = function (req) {
  var paramList = {
    follow: false,
    track: false,
    locations: false,
    delimited: false,
    stall_warnings: false
  };

  var rp = generateParamList(req, paramList);
  if (!rp.track && !rp.locations && !rp.follow) {
    throw constructErrorJSON("No filter parameters found. Expect at least one parameter: follow track locations", 406);
  } 

  var eventEmitter = new events.EventEmitter();
  streamHelper.apply(this, ["statuses/filter", rp, eventEmitter]);
  return eventEmitter;
};

TwitterHandler.prototype.sample = function (req) {
  var paramList = {
    delimited: false,
    stall_warnings: false
  };

  var eventEmitter = new events.EventEmitter()
    , rp = generateParamList(req, paramList);

  streamHelper.apply(this, ["statuses/sample", rp, eventEmitter]);
  return eventEmitter;
};

TwitterHandler.prototype.firehose = function (req) {
  var paramList = {
    count: false,
    delimited: false,
    stall_warnings: false
  };

  var eventEmitter = new events.EventEmitter()
    , rp = generateParamList(req, paramList);

  streamHelper.apply(this, ["statuses/firehose", rp, eventEmitter]);
  return eventEmitter;
};


module.exports = new TwitterHandler();
