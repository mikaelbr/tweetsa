
/*
 * GET home page.
 */
var sentiment = require('../lib/sentiment-provider');


exports.index = function(req, res){
  res.render('index', { title: 'Sentimental Analysis - Making the Twitter API more interesting.' });
};

exports.get = function (req, res) {
  // Example use of the sentiment cli
  sentiment.get("foo").on('data', function (data) {
    console.log('stdout: ' + data);
    res.render('index', { title: 'Sentimental Analysis - Response: ' + data })
  });
}