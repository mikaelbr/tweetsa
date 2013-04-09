define(['backbone', 'jquery', 'vent', 'highstock'], function(Backbone, $, vent) {
    Highcharts.setOptions({
     colors: ['rgb(255, 200, 200)', 'rgb(200, 255, 200)']
    });
    var State = Backbone.View.extend({
      tagName: 'figure',

      subtitleText: 'Total Tweets in State: ',

      initialize: function (options) {
        this.stateData = options.stateData;

        this.model.on('change:negative', this.negativeChange, this);
        this.model.on('change:positive', this.positiveChange, this);

        vent.on('map:reset', this.reset, this);

        $(this.stateData.hitArea.node).on('click', $.proxy(this.clicked, this));
        if (this.stateData.labelHitArea) {
          $(this.stateData.labelHitArea.node).on('click', $.proxy(this.clicked, this));
        }

        this.$el.width(270);
        this.$el.height(280);
      },

      reset: function () {
        this.chart = null;
        this.$el.html("");
      },

      _generateColor: function () {
        var pos = this.model.get('positive')
          , neg = this.model.get('negative')
          , sent = this.model.get('sentiment');

        if (sent === 0) {
          // return normal color
          return "#f5f5f5";
        }

        var posPercentage = (pos)/(pos+neg)
          , negPercentage = 1.0 - posPercentage
          , percentage = Math.max(posPercentage, negPercentage);

        posPercentage = Math.max(Math.min((posPercentage * 1.5) - 0.5, 1.0), 0);
        negPercentage = Math.max(Math.min((negPercentage * 1.5) - 0.5, 1.0), 0);
        var colorBase = Math.max(Math.min(Math.round(255*(1-percentage)), 255), 0)
          , inverted = (255 - colorBase);

        if (sent < 0) {
          // negative sentiment. return a redish color
          // return "rgba(255, " + colorBase + ", " + colorBase + ", " + percentage + ")";
          return "rgba(214, 60, 60, " + negPercentage + ")";
        }

        // positive sentiment. return a greenish color
        // return "rgba(" + colorBase + " , 255, " + colorBase + ", " + percentage + ")";
        return "rgba(117, 214, 60, " +  posPercentage + ")";
      },

      negativeChange: function (model, value, options) {
        this.fillState();
        this.updateChart();
      },

      positiveChange: function () {
        this.fillState();
        this.updateChart();
      },

      fillState: function () {
        var color = this._generateColor();
        this.stateData.shape.attr('fill', color);

        // ... for the label backing
        if(this.stateData.labelBacking) {
          this.stateData.labelBacking.attr('fill', color);
        }
      },

      updateChart: function () {
        if (this.$el.is(':visible') && this.model.hasChanged()) {
          this.render();
        }
        return this;
      },

      render: function () {
        if (this.model.get('negative') === 0 && this.model.get('positive') === 0) {
          this.$el.html('<p class="error-notice">No tweets in the state of ' + this.model.get('id') + ' yet.</p>');
          return this;
        }
        if (!this.chart) {
          this.generateChart();
        } else {
          this.updateChartDrawing();
        }

        return this;
      },

      clicked: function () {
        $('#stats').html(this.render().el);
      },

      generateChart: function () {
        this.chart = new Highcharts.Chart({
          chart: {
            // plotBackgroundColor: null,
            // plotBorderWidth: null,
            // plotShadow: false,
            renderTo: this.$el[0],
            animation: false,
            backgroundColor: null
          },
          title: {
            text: 'Total Sentiment for the state: ' + this.model.get('id')
          },
          tooltip: {
            headerFormat: '<span style="font-size: 10px">{series.name}</span><br/>',
            pointFormat: '{point.name}: <b>{point.percentage}%</b>',
            percentageDecimals: 1
          },
          subtitle: {
            text: this.subtitleText + (this.model.get('negative') + this.model.get('positive'))
          },
          plotOptions: {
            pie: {
              allowPointSelect: false,
              dataLabels: {
                enabled: true,
                distance: -50,
                color: '#000',
                formatter: function() {
                    return Highcharts.numberFormat(this.percentage, 1) + ' %';
                }
              },              
            },
            series: {
              animation: false
            }
          },
          series: [{
            type: 'pie',
            name: 'Sentiment',
            "color":"#C6D9E7",
            "borderColor":"#8BB6D9",
            "shadow":true,
            data: [
              ['Negative', this.model.get('negative')],
              ['Positive', this.model.get('positive')],
            ]
          }]
        });
      },

      updateChartDrawing: function () {
        this.chart.setTitle(null, {
          text: this.subtitleText + (this.model.get('negative') + this.model.get('positive'))
        });
        this.chart.series[0].setData([
          ['Negative', this.model.get('negative')],
          ['Positive', this.model.get('positive')],
        ], true);
      }
    });
   
    return State; 
});

