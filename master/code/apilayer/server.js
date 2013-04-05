
/**
 * Module dependencies.
 */
var util = require("util");
var express = require('express')
  , routes = require('./routes');

var app = module.exports = express.createServer();

// Configuration

app.enable("jsonp callback");

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

app.configure('production', function(){
  app.use(express.errorHandler());
});


routes.init(app);

app.listen(process.env.PORT || 8088);
console.log("Express server listening on port %d in %s mode", process.env.PORT || 8088, app.settings.env);
