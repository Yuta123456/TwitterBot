import tweepy
from util.twitter_api import *
from util.judge import *
from util.usr_info import update_user_information
import json
from util.judge import is_outliers


def learn_user_tweet(user_id, tweet):
    info = {"favorite_count": 0,
            "retweet_count": 0,
            "tweet_count": 0,
            "favorite_var": 0,
            "retweet_var": 0,
            "negative_count": 0}
    max_id = tweet.id
    for count in range(5):
        for tweet in fetch_tweet_by_user_id(count=200, screen_name=user_id, include_rts=False, exclude_replies=True):
            info = update_user_information(user_information=info, tweet=tweet)
    print("learned {}'s tweet".format(tweet.user.screen_name))
    return info
