import tweepy
from util.twitter_api import *
from util.judge import *
latest_tweet_id = None
for index, tweet in enumerate(fetch_tweet(count=200, since_id=latest_tweet_id, exclude_replies=True, include_rts=False)):
    print(tweet.id)
