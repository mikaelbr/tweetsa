"""
    The first layer of classifing. Check the polarity of a tweet.
"""

from base import *

class Sentiment(BaseLayer):

    def __init__(self, training_set_filename, filters, feature_extraction):
        super(Sentiment, self).__init__(training_set_filename, filters, feature_extraction)

    def classify(self, json_obj):
        tweet = self.filters(json_obj)
        features = self.feature_extraction(tweet);
        