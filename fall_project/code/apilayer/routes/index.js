
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'Sentimental Analysis - Making the Twitter API more interesting.' })
};