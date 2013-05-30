$(function () {
    function search(query, count, callback) {
        var query = encodeURI(query);
        console.log(query);
        $.ajax({
            dataType: "jsonp", 
            url: 'http://gribb.dyndns.org:8088/search/tweets.json?q=' + query + '&lang=en&count=' + count,
            success: function(data) {
                callback(data);
            },
            error: function() {
                //$renderTo.html("Sorry, an error occured.");
                console.log('failed');
            }
        });
    }

    function sortTweets(tweets, callback) {
        var sentiment = {
            positive: 0,
            neutral: 0,
            negative: 0
        };
        var color = '#FFFFFF';
        for(var i=0;i<tweets.length;i++) {
            if(tweets[i].sentiment.classification === 'positive') {
                sentiment.positive++;
                color = '#7ccd24';
            }
            else if(tweets[i].sentiment.classification === 'neutral') {
                sentiment.neutral++;
                color = '#b2c4f0';
            }
            else if(tweets[i].sentiment.classification === 'negative') {
                sentiment.negative++;
                color = '#ff4e50';
            }
            generateStatusHtml(tweets[i], color);
        }
        console.log(sentiment);
        callback(sentiment);
    }

    function generateStatusHtml(tweet, color) {
        $('#status-container').prepend('<div id='+tweet.id_str+' class="status-container" style="background-color:'+color+';display:none;"><img id="img-'+tweet.id_str+'" src="'+tweet.user.profile_image_url+'"/>' + tweet.text + '<span class="status-date">' + parseTwitterDate(tweet.created_at)+'</span></div>');
        $('#img-'+tweet.id_str).on('load', function () {
            $('.bar').hide();
            $('#'+tweet.id_str+'').show();
        });
    }

    function parseTwitterDate(text) {
        var newtext = text.replace(/(\+\S+) (.*)/, '$2 $1');
        var date = new Date(Date.parse(newtext)).toLocaleDateString();
        var time = new Date(Date.parse(newtext)).toLocaleTimeString();
        return date +', ' + time;
    }

    function getPercent(num, tot) {
        if (tot > 0)return (num/tot*100).toFixed(1);
        return 0;
    }

    function renderChart(query, tweets) {
         var red = '#ff4e50', green = '#7ccd24', gray = '#bbd0fb';
    // Insert data
        var pos = [tweets.positive], neutral = [tweets.neutral], neg = [tweets.negative];
        var tot = pos[0]+neutral[0]+neg[0];
        $('#total-tweet-count').text(tot);
        $('#keyword').text(query);
        $('#chart').highcharts({
            chart: {
            },
            title: {
                text: 'Twitter Sentiment'
            },
            xAxis: {
                categories: ['Tweets']
            },
            tooltip: {
                formatter: function() {
                    var s;
                    if (this.point.name) { // the pie chart
                        s = ''+
                            this.point.name +': '+ getPercent(this.y, tot) +'%';
                    } else {
                        s = ''+
                            this.x  +': '+ this.y;
                    }
                    return s;
                }
            },
            labels: {
                items: [{
                    // html: 'Number of tweets: '+ tot,
                    style: {
                        left: '40px',
                        top: '8px',
                        color: 'black'
                    }
                }]
            },
            series: [{
                type: 'column',
                name: 'Positive',
                color: green,
                data: pos
            }, {
                type: 'column',
                name: 'Neutral',
                color: gray,
                data: neutral
            }, {
                type: 'column',
                name: 'Negative',
                color: red,
                data: neg
            }, {
                type: 'pie',
                name: 'Total consumption',
                data: [{
                    name: 'Positive',
                    color: green,
                    y: pos[0],
                }, {
                    name: 'Neutral',
                    color: gray,
                    y: neutral[0],
                }, {
                    name: 'Negative',
                    color: red,
                    y: neg[0],
                }],
                center: [45, 45],
                size: 100,
                showInLegend: false,
                dataLabels: {
                    enabled: false
                }
            }]
        });
    }

    $('body').on('submit', '#search-form', function (e) {
        console.log('bar');
        $('#status-container').empty();
        $('.bar').show();
        e.preventDefault();
        var query = $('#tweet-search').val();
        var count = $('#tweet-count').val();
        search(query, count, function(data) {
            console.log('fetching data..' + count + ' tweets');
            console.log(data);
            sortTweets(data, function(sorted) {
                console.log('rendering data..');
                renderChart(query, sorted);
            });    
        });   
    }) 
});
    
