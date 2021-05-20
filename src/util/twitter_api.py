import tweepy
import os
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

USER_ID = "doNotSpeakIll"
"""
Parameters:	
count – The number of results to try and retrieve per page.
since_id – Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
max_id – Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.
trim_user – A boolean indicating if user IDs should be provided, instead of complete user objects. Defaults to False.
exclude_replies – This parameter will prevent replies from appearing in the returned timeline. Using exclude_replies with the count parameter will mean you will receive up-to count Tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.
include_entities – The entities node will not be included when set to false. Defaults to true.
"""


def fetch_tweet(count=20, since_id=None, max_id=None, trim_user=False, exclude_replies=False, include_entities=True, include_rts=True):
    return api.home_timeline(count=count, since_id=since_id, max_id=max_id, trim_user=trim_user, exclude_replies=exclude_replies, include_entities=include_entities, include_rts=include_rts)


"""
Parameters:	
user_id – Specifies the ID of the user. Helpful for disambiguating when a valid user ID is also a valid screen name.
screen_name – Specifies the screen name of the user. Helpful for disambiguating when a valid screen name is also a user ID.
since_id – Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
count – The number of results to try and retrieve per page.
max_id – Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.
trim_user – A boolean indicating if user IDs should be provided, instead of complete user objects. Defaults to False.
exclude_replies – This parameter will prevent replies from appearing in the returned timeline. Using exclude_replies with the count parameter will mean you will receive up-to count Tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.
include_rts – When set to false, the timeline will strip any native retweets (though they will still count toward both the maximal length of the timeline and the slice selected by the count parameter). Note: If you’re using the trim_user parameter in conjunction with include_rts, the retweets will still contain a full user object.
"""


def fetch_tweet_by_user_id(user_id=None, screen_name=None,
                           since_id=None, max_id=None, count=20, trim_user=False, exclude_replies=False, contributor_details=True, include_rts=True):
    if (not user_id and not screen_name):
        print("Must assign user_id or screen_name")
        return
    return api.user_timeline(user_id=user_id, screen_name=screen_name, since_id=since_id, max_id=max_id, count=count,
                             trim_user=trim_user, exclude_replies=exclude_replies, contributor_details=contributor_details, include_rts=include_rts)


def follow_back():
    # Cursorを使ってフォロワーのidを逐次的に取得
    followers_ids = api.followers_ids()
    print("followers:{}".format(followers_ids))
    friends = api.friends_ids(USER_ID)
    for followers_id in followers_ids:
        # 全てのフォロワーをフォロー
        if followers_id not in friends:
            hello_user = api.get_user(followers_id)
            api.update_status(create_hello_text(
                hello_user.screen_name, hello_user.name))
            api.create_friendship(followers_id)


def unfollow():
    followers = api.followers_ids(USER_ID)
    friends = api.friends_ids(USER_ID)
    for usr_id in friends:
        if usr_id not in followers:
            goodbye_user = api.get_user(usr_id)
            goodbye_user_screen_name = goodbye_user.screen_name
            api.update_status(create_goodbye_text(goodbye_user_screen_name))
            api.destroy_friendship(usr_id)


def reply_bad_people(tweet):
    bad_people = tweet.user.screen_name
    try:
        api.update_status(create_message_to_bad_people(
            bad_people), in_reply_to_status_id=tweet.id)
    except tweepy.error.TweepError:
        print("ツイートが重複しています。")


def create_message_to_bad_people(screen_name):
    return "@" + screen_name + "\n人の悪口を言わない"


def reply_good_people(tweet):
    good_people = tweet.user.screen_name
    api.update_status(create_message_to_good_people(
        good_people), in_reply_to_status_id=tweet.id)


def create_message_to_good_people(screen_name):
    return "@" + screen_name + "\nそういうツイートばっかりしろ"


def create_goodbye_text(screen_name):
    return "@" + screen_name + "\n" + "使ってくれてありがとう！"


def create_hello_text(screen_name, user_name):
    return "@" + screen_name + "\n" + "こんにちは" + user_name + "さん！\n" + "人の悪口を言ったときに反応するよ！"
