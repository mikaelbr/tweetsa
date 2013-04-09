define(
    ['backbone', 'jquery']
  , function(Backbone, $) {
  

  var backgrounds = [
    '461-1223013714msB6',
    '1-1275673689tHg9',
    '1-1275673689tHg9',
    '461-1223013714msB6',
    'America-seen-from-orbit1284',
    'Frozen-reservoir-in-the-mountains799',
    'Mountain-spring-landscape734',
    'Palm-tree-forest659',
    'Spring-over-the-mountains1678'
  ];

  var BackgroundLoader = Backbone.View.extend({
    el: 'html',
    numSecBeforeSwitch: 30,
    animationTimeInMS: 1000,

    start: function() {
      this.interval = setInterval($.proxy(this.setRandomBackground, this), this.numSecBeforeSwitch * 1000);
      return this;
    },

    stop: function () {
      clearInterval(this.interval);
      this.interval = null;
      return this;
    },

    setRandomBackground: function () {
      var $htmlEl = this.$el
        , $bgEl = $('#background-1')
        , randImg = backgrounds[Math.floor(Math.random()*backgrounds.length)]
        , that = this;

      if ($bgEl.is(':visible')) {
        // Fade out bgEl, show html bg
        $htmlEl.css('backgroundImage', 'url("img/' + randImg + '.jpg")');
        setTimeout(function () {
          $bgEl.fadeOut(that.animationTimeInMS);
        }, 1000);
      } else {
        // Set bg on bgEl, show bgEl
        $bgEl.css('backgroundImage', 'url("img/' + randImg + '.jpg")');
        setTimeout(function () {
          $bgEl.fadeIn(that.animationTimeInMS);
        }, 1000);
      }
      return this;
    }

  });

  return BackgroundLoader;
});