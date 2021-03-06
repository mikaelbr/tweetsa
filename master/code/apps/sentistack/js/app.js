;(function ($, undefined) {

  var methods = {
    queries: [],
    data: {},
    series: [],
    count: 100,

    url: 'http://gribb.dyndns.org:8088/search/tweets.json?q=',

    init: function () {
      this.bindEvents();
    },

    bindEvents: function () {
      $('#appendQuery').on('click', $.proxy(this.appendQueryInput, this));
      $('form').on('submit', $.proxy(this.formSubmitted, this));
      $('.hide-button').on('click', this.toggleList);
    },

    toggleList: function (e) {
      e.preventDefault();
      var height = 60;
      var $field = $('.input-wrap');

      if ($field.height() > height) {
        // hide
        $field.css('overflow', 'hidden').height(height);
      } else {
        $field.css('overflow', 'auto').height('auto');
      }
      return this;
    },

    reset: function () {
      $('#container').html('');
      this.queries = [];
      this.data = [];
      this.series = [];
    },

    formSubmitted: function (e) {
      e.preventDefault();
      var that = this;
      this.reset();
      this.loadGeneratingGraphText();

      $('.query').each(function () {
        that.addQuery(this.value);
      });
      that.search();
      return false;
    },

    appendQueryInput: function (e) {
      e.preventDefault();
      var $origEl = $('.query').last(),
          el = $origEl.clone().val('');
      $origEl.after(el);
      el.focus()
      return false;
    },

    addQuery: function (query) {
      if (query && query.length > 0) {
        this.queries.push(query);
      }
    },

    fetch: function (query) {
      query = encodeURI(query);
      return $.ajax({
        dataType: "jsonp", 
        url: this.url + query + '&lang=en&count=' + this.count,
        error: function() {
          console && console.error('failed');
        }
      });
    },

    fetchMore: function (query, cb) {
      var def = $.Deferred();
      var that = this;
      this.fetch(query).done(function (data) {
        var max_id = data[data.length - 1].id;
        query = encodeURI(query);

        $.ajax({
          dataType: "jsonp", 
          url: that.url + query + '&lang=en&count=' + that.count + '&max_id=' + max_id,
          error: function() {
            def.reject();
          }
        }).done(function (second) {
          if (!second) {
            def.reject();
          }
          def.resolve(data.concat(second));
        }).fail(function () {
          def.reject();
        });
      });
      return def;
    },

    search: function () {
      var numQueries = this.queries.length,
          that = this,
          _n = 0;
      $.each(this.queries, function(i, query) {
        that.fetchMore(query).done(function (data) {
          that.data[query] = that.constructData(data);
        }).always(function() { 
          if (++_n === numQueries) {
            that.constructGraph();
          }          
        })
      });
    },

    constructData: function (tweets) {
      var sentiment = {
          positive: 0,
          neutral: 0,
          negative: 0
      };

      console.log(tweets);

      for(var i=0;i<tweets.length;i++) {
        var classific = tweets[i].sentiment.classification;
        if(classific === 'positive') {
          sentiment.positive++;
        }
        else if(classific === 'neutral') {
          sentiment.neutral++;
        }
        else if(classific === 'negative') {
          sentiment.negative++;
        }
      }
      return sentiment;
    },

    generateColor: function (sentiment) {
      if(sentiment === 'positive') {
        return 'rgb(200, 255, 200)';
      }
      
      if(sentiment === 'neutral') {
        return 'gray';
      }
      
      if(sentiment === 'negative') {
        return 'rgb(255, 200, 200)';
      }
    },

    constructSeries: function () {
      var that = this;
      // $.each(['negative', 'positive'], function (i, sent) {
      $.each(['neutral', 'negative', 'positive'], function (i, sent) {
        var data = [];
        $.each(that.queries, function(i, query) {
          data.push(that.data[query][sent]);
        });
        that.series.push({
          name: sent,
          data: data,
          color: that.generateColor(sent)
        });
      });
    },

    loadGeneratingGraphText: function () {
      $('#container').html('<p class="loading">Generating Graph</p>');
    },

    constructGraph: function () {
      this.constructSeries();
      $('#container').highcharts({
        chart: {
          type: 'column'
        },
        title: {
          text: 'Sentiment Comparison'
        },
        xAxis: {
          categories: this.queries
        },
        yAxis: {
          min: 0,
          title: {
              text: 'Sentiment Percentage'
          }
        },
        tooltip: {
          pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
          shared: true
        },
        plotOptions: {
          column: {
              stacking: 'percent'
          }
        },
        series: this.series
      });
    }
  };

  methods.init();
    
}(jQuery));

/*

*/