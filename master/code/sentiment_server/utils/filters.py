"""
    A collection of different filter methods for the tweets.
"""
import re

# Emoticon definitions.
NormalEyes = r'[:=]'
Wink = r'[;]'
NoseArea = r'(|o|O|-)'
HappyMouths = r'[D\)\]]'
SadMouths = r'[\(\[]'
Tongue = r'[pP]'
OtherMouths = r'[doO/\\]'
Happy_RE = re.compile('(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')', re.UNICODE)
Sad_RE = re.compile(NormalEyes + NoseArea + SadMouths,  re.UNICODE)

Wink_RE = re.compile(Wink + NoseArea + HappyMouths,  re.UNICODE)
Tongue_RE = re.compile(NormalEyes + NoseArea + Tongue,  re.UNICODE)
Other_RE = re.compile('(' + NormalEyes + '|' + Wink + ')' + NoseArea + OtherMouths, re.UNICODE)

Emoticon = (
    "(" + NormalEyes + "|" + Wink + ")" + NoseArea +
    "(" + Tongue + "|" + OtherMouths + "|" + SadMouths + "|" + HappyMouths + ")"
)
Emoticon_RE = re.compile(Emoticon,  re.UNICODE)

# Username definitions
usernames = r'(@[a-zA-Z0-9_]{1,15})'


# Hashtag definitions
hashtags = r'(#[a-zA-Z]+[a-zA-Z0-9_]*)'
hashtags_filter = r'(#([a-zA-Z]+[a-zA-Z0-9_]*))'


# RT definitions
rt_tag = r'(^RT\s+|\s+RT\s+)'


# URL definitions
url = r'(\w+:\/\/\S+)'
url_re = re.compile(url,  re.UNICODE)

def no_emoticons(tweet_text):
    tweet = re.sub(Happy_RE, "", tweet_text)
    tweet = re.sub(Sad_RE, "", tweet)
    tweet = re.sub(Emoticon_RE, "", tweet)
    return tweet.lower().strip()

def no_usernames(tweet_text):
    tweet = re.sub(usernames, "", tweet_text)
    return tweet.lower().strip()

def username_placeholder(tweet_text):
    return re.sub(usernames, "||U||", tweet_text).lower()

def no_hash(tweet_text):
    tweet = re.sub(hashtags, "", tweet_text)
    return tweet.strip().lower()

def hash_placeholder(tweet_text):
    return re.sub(hashtags, "||H||", tweet_text).lower()

def hash_as_normal(tweet_text):
    return re.sub(r'#([a-zA-Z]+[a-zA-Z0-9_]*)', "\\1", tweet_text)

def no_rt_tag(tweet_text):
    tweet = re.sub(rt_tag, "", tweet_text)
    return tweet.strip().lower()

def no_url(tweet_text):
    tweet = re.sub(url, "", tweet_text)
    return tweet.strip().lower()

def url_placeholder(tweet_text):
    return re.sub(url, "||URL||", tweet_text).lower()

def reduce_letter_duplicates(tweet_text):
    return re.sub(r'(.)\1{3,}', r'\1\1\1', tweet_text, flags=re.IGNORECASE).lower()
