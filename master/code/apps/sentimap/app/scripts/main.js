require.config({
  paths: {
    'jquery': 'vendor/jquery/jquery',
    'underscore': 'vendor/underscore-amd/underscore',
    'backbone': 'vendor/backbone-amd/backbone',
    'usmap': 'libs/jquery.us-map',
    'raphael': 'vendor/raphael/raphael',
    'eve': 'vendor/eve-adobe/eve',
    'highcharts': 'libs/highcharts',
    'highstock': 'libs/highstock',
  },
  shim: {
    'usmap': ['jquery', 'raphael'],
    'raphael': ['eve'],
    'highcharts': ['jquery'],
    'highstock': ['jquery']
  }
});

require(['views/app'], function(AppView) {

  window.app = new AppView;
});