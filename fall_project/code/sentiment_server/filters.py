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
usernames = r'((^@[^\s]+)|\s+@[^\s]+)'
username_re = re.compile(usernames,  re.UNICODE)


# Hashtag definitions
hashtags = r'((^#[^\s]+)|\s+#[^\s]+)'
hashtags_re = re.compile(hashtags,  re.UNICODE)


# RT definitions
rt_tag = r'(^RT\s+|\s+RT\s+)'
rt_tag_re = re.compile(rt_tag,  re.UNICODE)


# URL definitions
url = r'(\s+\w+:\/\/\S+)'
url_re = re.compile(url,  re.UNICODE)


def no_emoticons(tweet_text):
    tweet = re.sub(Happy_RE, "", tweet_text)
    tweet = re.sub(Sad_RE, "", tweet)
    tweet = re.sub(Emoticon_RE, "", tweet)
    return tweet.strip()


def no_usernames(tweet_text):
    tweet = re.sub(username_re, "", tweet_text)
    return tweet.strip()


def no_hash(tweet_text):
    tweet = re.sub(hashtags_re, "", tweet_text)
    return tweet.strip()


def no_rt_tag(tweet_text):
    tweet = re.sub(rt_tag_re, "", tweet_text)
    return tweet.strip()


def no_url(tweet_text):
    tweet = re.sub(url_re, "", tweet_text)
    return tweet.strip()
