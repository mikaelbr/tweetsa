
/*
 * GET home page.
 */
var sentiment = require('../lib/sentiment-provider')
  , twitter = require('../lib/twitter-handler');


var responseHandle = function (err, data, res) {
  res.contentType('application/json');
  if (err) {
    var errorCode = 200;
    if ( err.errors ) {
      errorCode = err.errors[0].code || 200;
    }

    res.send(err, errorCode);
    return false;
  } 

  res.send(data);
};


exports.index = function(req, res){
  res.render('index', { title: 'Sentimental Analysis - Making the Twitter API more interesting.' });
};

exports.get = function (req, res) {
  // Example use of the sentiment cli
  sentiment.get("foo").on('data', function (data) {
    console.log('stdout: ' + data);
    res.render('index', { title: 'Sentimental Analysis - Response: ' + data });
  });
};


exports.search = function (req, res) {
  var start = +new Date();
  twitter.search(req, function (err, data) {
    responseHandle(err, data, res);
    var end = +new Date();
    console.log("Done in " + (end-start)/1000 + " seconds");

  });
};