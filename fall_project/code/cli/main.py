"""
    Running a sentimental analysis on a tweet JSON Object.

    Input: A string serialized JSON object from the Twitter API
    Output: string <neutral, positive, negative>
"""
import random
import logging
import sys

if __name__ == "__main__":

    import argparse

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

    args = parser.parse_args()


    
    level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    twitter_string = args.tweet

    logging.debug("Choosing a result")
    print random.choice(["positive", "negative", "neutral"])

