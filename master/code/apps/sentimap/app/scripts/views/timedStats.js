define(['backbone', 'underscore', 'jquery', 'vent', 'highstock'], function(Backbone, _, $, vent) {

    var Stats = Backbone.View.extend({
      el: '#overall-stats',

      currentPositiveAcc: 0,
      currentNegativeAcc: 0,

      statsIntervalTimeInMS: 1000,

      initialize: function (options) {
        this.model.on('change', this.addPoint, this);
        vent.on('map:reset', this.reset, this);

        vent.on('tweet:positive', this.positiveTweet, this);
        vent.on('tweet:negative', this.negativeTweet, this);

        this.initStatsInterval();
      },

      reset: function () {
        this.chart = null;
        this.$el.html("");
      },

      positiveTweet: function () {
        this.currentPositiveAcc += 1;
      },

      negativeTweet: function () {
        this.currentNegativeAcc += 1;
      },

      addStatsToModel: function () {
        this.model.pushData(this.currentPositiveAcc, this.currentNegativeAcc);
        this.currentPositiveAcc = 0;
        this.currentNegativeAcc = 0;
      },

      initStatsInterval: function () {
        setInterval($.proxy(this.addStatsToModel, this), this.statsIntervalTimeInMS);
      },

      addPoint: function () {
        if (!this.chart) {
          return;
        }

        var serie = this.chart.series[0];
        serie.addPoint(_.last(this.model.get('data')), true, true);
      },

      render: function () {
        this.generateChart();
        return this;
      },

      reset: function () {
        this.chart = null;
        this.model.set('data', []);
        this.currentPositiveAcc = 0;
        this.currentNegativeAcc = 0;
        this.generateChart();
      },

      generateChart: function () {
        var startUpPlaceholderData = (function() {
          // generate an array of random data
          var data = [], time = (new Date()).getTime(), i;

          for( i = -600; i <= 0; i++) {
            data.push([ time + (i * 1000), 0 ]);
          }
          return data;
        })();
        // set up the updating of the chart each second
        this.chart = new Highcharts.StockChart({
          
          chart: {
            renderTo: this.el,
            backgroundColor: null
          },

          global: {
            useUTC: false
          },

          rangeSelector: {
            enabled: false
          },

          title : {
            enabled: false
          },

          navigator: {
            enabled: false
          },
          scrollbar: {
            enabled: false
          },

          yAxis: {
            labels: {
              enabled: false
            },
            gridLineWidth: 0
          },

          xAxis: {
            labels: {
              enabled: false
            }
          },

          series : [{
            name : 'Sentiment Difference',
            // data : data,
            data : startUpPlaceholderData,
            type : 'areaspline',
            // threshold : null,
            // tooltip : {
            //   valueDecimals : 2
            // },
            color: '#396DBF',
            fillColor : "rgba(0,0,0, 0.4)"
            // // fillColor : "rgba(136, 191, 232, 0.4)"
          }]
        });
      }
    });
   
    return Stats; 
});

