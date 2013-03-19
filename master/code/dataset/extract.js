
var fs = require('fs');

var userStats = {};

var extractLabel = function (classification) {

  if (classification.length < 2) {
    if ( !userStats[classification[0].user] ) {
      userStats[classification[0].user] = 0;
    }

    userStats[classification[0].user]++;
    return classification[0].value === "objective" ? "neutral" : classification[0].value;
  }

  var votes = {
    "objective": 0,
    "positive": 0,
    "negative": 0
  };

  for (var i = 0, len = classification.length; i < len; i++) {
    vote = classification[i];

    if ( !userStats[vote.user] ) {
      userStats[vote.user] = 0;
    }
    userStats[vote.user]++;

    votes[vote.value]++;
  }

  var max = 0, bestVote = "";

  for (v in votes) {
    var num = votes[v];
    if (num >= max) {
      bestVote = v;
      max = num;
    }
  }

  if (bestVote === "objective") {
    bestVote = "neutral";
  }

  return bestVote;
};

var formatTweet = function (tweet) {
  return tweet.id + "\t" + 
          tweet.user.id + "\t" +
          extractLabel(tweet.annotation.classification) + "\t" + 
          tweet.text.replace(/\n/g,  "");

};

fs.readFile('data.json', function (err, data) {
  var jsonData = JSON.parse(data.toString());
  jsonData.forEach(function (obj) {
    console.log(formatTweet(obj));
  });

  // console.log("Information: ");
  // console.log("1. Length: ", jsonData.length)
  // console.log("1. User Stats: ", userStats)
});