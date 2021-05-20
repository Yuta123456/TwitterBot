# 四時間に一回これが走る
import tweepy
from util.twitter_api import *
from util.judge import *
from util.usr_info import update_user_information
import json
from util.judge import is_outliers
from learn import learn_user_tweet
# フォローしてくれた人にフォロー返す
follow_back()
# フォロー外した人はフォロー外す
unfollow()

json_open = open('./src/data/data.json', 'r')
json_load = json.load(json_open)
latest_tweet_id = json_load["latest_tweet_id"]
for index, tweet in enumerate(fetch_tweet(count=200, since_id=latest_tweet_id, exclude_replies=True, include_rts=False)):
    if index == 0:
        # 最新のものに更新
        json_load["latest_tweet_id"] = tweet.id
    user_id = tweet.user.screen_name
    if user_id not in json_load:
        json_load[user_id] = learn_user_tweet(user_id, tweet)
    # 外れ値でないならユーザの情報を更新
    if not is_outliers(tweet, json_load[user_id]):
        json_load[user_id] = update_user_information(json_load[user_id], tweet)

    user_info = json_load[user_id]

    if is_bad_word_for_people(tweet, user_info):
        reply_bad_people(tweet)
        user_info["negative_count"] += 1
    # ネガティブなツイートがたまってる中で、ポジティブなツイートしたときは
    # そういうツイートばっかりするように催促
    if is_positive_word(tweet) and is_popular_tweet(tweet, json_load[user_id]) and json_load[user_id]["negative_count"] >= 5:
        reply_good_people(tweet)
        user_info["negative_count"] = 0
    json_load[user_id] = user_info
with open('./src/data/data.json', mode='wt', encoding='utf-8') as file:
    json.dump(json_load, file, ensure_ascii=False, indent=4)
