
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

exports.search = function (req, res) {
  var start = +new Date();
  twitter.search(req, function (err, data) {
    responseHandle(err, data, res);
    var end = +new Date();
    console.log("Done in " + (end-start)/1000 + " seconds");
  });
};

exports.filterStream = function (req, res) {
  res.contentType('application/json');

  
  var stream;
  try {
    stream = twitter.statusesFilter(req);
  } catch(e) {
    responseHandle(e, null, res);
    return;
  }

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