""" 
    Base layer for classifying tweets.
"""

class BaseLayer(object):

    def __init__(self, training_set_filename, filters, feature_extraction):
        self.training_set_filename = training_set_filename
        self.filters = filters
        self.feature_extraction = feature_extraction