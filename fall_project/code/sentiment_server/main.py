#!/usr/bin/python

"""
    A POST Server running a sentimental analysis on a tweet
    stringified JSON Object.

    Takes POST requests and returns a string with the classification.
    Classification scheme: <neutral, positive, negative>
"""
import logging
import sys
import argparse
import simplejson as json


# Server used..
import eventlet


# Do import of all different methods here:
# Remember: When adding a new method, add it to the methods/__init__.py
from methods import *

# the pool provides a safety limit on our concurrency
pool = eventlet.GreenPool(size=10000)


def init_app(classifier_class):
    """
        Initialize the POST server functions.
    """
    # Using closure to provide classifier
    def get_sentiment(tweet):
        return classifier_class.run(json.loads(tweet))

    def app(environ, start_response):

        if environ['REQUEST_METHOD'] != 'POST':
            start_response('403 Forbidden', [])
            return []
        # the pile collects the result of a concurrent operation -- in this case,
        # the collection of feed titles
        pile = eventlet.GreenPile(pool)
        data = environ['wsgi.input'].read()
        for line in data.split('\n'):
            tweet = line.strip()
            if tweet:
                pile.spawn(get_sentiment, tweet)
        # since the pile is an iterator over the results,
        # you can use it in all sorts of great Pythonic ways
        tweets = '\n'.join(pile)
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [tweets + "\r\n"]

    return app


def str_to_class(field):
    """
        Used to convert string to a class. For giving a class as an argument.
    """
    try:
        identifier = getattr(sys.modules[__name__], field)
    except AttributeError:
        raise NameError("%s doesn't exist." % field)
    if isinstance(identifier, type):
        return identifier
    raise TypeError("%s is not a class." % field)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(version='0.1', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--debug',
                dest='debug',
                action='store_true',
                default=False,
                help='Show debug data.')

    parser.add_argument('-m', '--method',
                dest='method_name',
                action='store',
                default='AFINN',
                help='Show debug data. Default value "AFINN"')

    parser.add_argument('-p', '--port',
                dest='port',
                type=int,
                action='store',
                default=7000,
                help='Server port. Default value 7000.')

    args = parser.parse_args()

    # Set logging settings.
    level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    # Start server
    from eventlet import wsgi
    wsgi.server(eventlet.listen(('localhost', args.port)), init_app(str_to_class(args.method_name)))

