var util     = require('util')
  , events  = require('events');

// Constructor
var TwitterHandler = function () {
    if(false === (this instanceof TwitterHandler)) {
      return new TwitterHandler();
    }

    // Use emitter or not? Maybe emitting isn't the best solution for this.
    events.EventEmitter.call(this);
    this.init();
};

util.inherits(TwitterHandler, events.EventEmitter);


// Private functions? 


// Prototype methods
TwitterHandler.prototype.init = function () {
    // Do some initialization.


};

// etc...



module.exports = new TwitterHandler();
