"""
    The first layer of classifing. Check the polarity of a tweet.
"""

from base import *

class Polarity(BaseLayer):

    def __init__(self, training_set_filename, filters, feature_extraction):
        super(Polarity, self).__init__(training_set_filename, filters, feature_extraction)

    def classify(self, json_obj):
        pass