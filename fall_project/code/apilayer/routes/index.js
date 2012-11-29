
/*
 * GET home page.
 */
var sentiment = require('../lib/sentiment-provider')
  , twitter = require('../lib/twitter-handler');


var APIController = function APIController () {


};

exports.APIController = APIController;

exports.init = function (app) {
  var ct = new APIController();


  // Routes
  app.get('/search/tweets.json', ct.search);
  app.get('/statuses/retweets/:id.json', ct.retweets);
  app.get('/statuses/show.json', ct.show);
  app.get('/favorites/list.json', ct.favorites);


  app.get('/statuses/filter.json', ct.filterStream);
  app.get('/statuses/sample.json', ct.sample);
  app.get('/statuses/firehose.json', ct.firehose);


  app.get('/lists/statuses.json', ct.lists);
  app.get('/lists/show.json', ct.listsShow);
};


var responseHandle = function (err, data, res) {
  if (err) {
    var errorCode = 200;
    if ( err.errors ) {
      errorCode = err.errors[0].code || 200;
    }

    res.contentType('application/json');
    res.send(err, errorCode);
    return false;
  } 

  res.json(data);
};

var routesHelper = function (method) {
  return function (req, res) {
    var start = +new Date();
    twitter[method](req, function (err, data) {
      responseHandle(err, data, res);
      var end = +new Date();
      console.log("Entire lookup, done in " + (end-start)/1000 + " seconds");
    });
  }
}

APIController.prototype.search = routesHelper("search");
APIController.prototype.retweets = routesHelper("retweets");
APIController.prototype.show = routesHelper("show");

APIController.prototype.favorites = routesHelper("favorites");

APIController.prototype.lists = routesHelper("lists");
APIController.prototype.listsShow = routesHelper("listsShow");


APIController.prototype.filterStream = function (req, res) {
  res.contentType('application/json');

  var stream;
  try {
    stream = twitter.statusesFilter(req);
  } catch(e) {
    responseHandle(e, null, res);
    return;
  }

  // When the client stoppes listening, stop fetching data.
  req.connection.addListener('close', function () {
    stream.destroy();
  });

  stream.on('data', function (item) {
    res.write(JSON.stringify(item) + '\n');
  })
  .on('error', function (error) {
    responseHandle(error, null, res);
  })
  .on('end', function (response) {
    res.end();
  });
};

APIController.prototype.sample = function (req, res) {
  res.contentType('application/json');
  
  var stream = twitter.sample(req);

  // When the client stoppes listening, stop fetching data.
  req.connection.addListener('close', function () {
    stream.destroy();
  });

  stream.on('data', function (item) {
    res.write(JSON.stringify(item) + '\n');
  })
  .on('error', function (error) {
    responseHandle(error, null, res);
  })
  .on('end', function (response) {
    res.end();
  });
};


APIController.prototype.firehose = function (req, res) {
  res.contentType('application/json');
  
  var stream = twitter.firehose(req);

  // When the client stoppes listening, stop fetching data.
  req.connection.addListener('close', function () {
    stream.destroy();
  });

  stream.on('data', function (item) {
    res.write(JSON.stringify(item) + '\n');
  })
  .on('error', function (error) {
    responseHandle(error, null, res);
  })
  .on('end', function (response) {
    res.end();
  });
};


