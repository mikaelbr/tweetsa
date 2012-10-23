"""
    Running a sentimental analysis on a tweet JSON Object.

    Input: A string serialized JSON object from the Twitter API
    Output: string <neutral, positive, negative>
"""
import logging
import sys
import types
import argparse

# Do import of all different methods here:
# Remember: When adding a new method, add it to the methods/__init__.py
from methods import *


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

    parser.add_argument("tweet", 
                metavar="TWEET",
                type=str,
                help="The Tweet in stringified JSON form.")

    parser.add_argument('-d', '--debug', 
                dest='debug', 
                action='store_true',
                default=False,
                help='Show debug data.')

    parser.add_argument('-m', '--method', 
                dest='method_name', 
                action='store',
                default='BasicBigram',
                help='Show debug data.')

    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    print str_to_class(args.method_name).run(args.tweet)

