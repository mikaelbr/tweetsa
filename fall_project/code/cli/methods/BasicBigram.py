"""
    Sentiment analysis using basic bigrams.
"""

import logging
import random

from BaseMethod import BaseMethod

class BasicBigram(BaseMethod):
    
    @staticmethod
    def run(arg_input):
        logging.debug("Doing basic bigram")
        return random.choice(["positive", "negative", "neutral"])