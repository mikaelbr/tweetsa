"""
    Sentiment analysis using AFINN.
"""
import math
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging

from base import BaseMethod
import filters as filt


# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = './data/AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ws.strip().split('\t') for ws in open(filenameAFINN)]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")


class AFINN(BaseMethod):


    @staticmethod
    def filter(tweet):
        tweet = filt.no_url(tweet)
        tweet = filt.no_rt_tag(tweet)
        tweet = filt.no_emoticons(tweet)
        tweet = filt.no_usernames(tweet)
        tweet = filt.no_hash(tweet)

        logging.debug("--- FINISHED FILTERING: %s" % tweet)

        return tweet

    @staticmethod
    def sentiment(tweet_text):
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence.
        """
        words = pattern_split.split(tweet_text.lower())
        sentiments = map(lambda word: afinn.get(word, 0), words)
        if sentiments:
            # How should you weight the individual word sentiments?
            # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
            sentiment = float(sum(sentiments)) / math.sqrt(len(sentiments))
        else:
            sentiment = 0
        return sentiment


    @staticmethod
    def run(tweet):
        logging.debug("Doing AFINN classification")
        filtered_tweet = AFINN.filter(tweet['text'])
        sentiment = AFINN.sentiment(filtered_tweet)

        logging.debug("--- Found sentiment: %6.2f for tweet:  %s" % (sentiment, filtered_tweet))

        if sentiment > 0:
            return "positive"

        if sentiment < 0:
            return "negative"

        return "neutral"
