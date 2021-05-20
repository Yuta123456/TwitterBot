

def update_user_information(user_information, tweet):

    # ツイートの情報を取得
    tweet_fav_count = tweet.favorite_count
    tweet_rt_count = tweet.retweet_count

    # ユーザの情報を取得
    usr_tweet_cnt = user_information["tweet_count"]
    usr_fav_cnt = user_information["favorite_count"]
    usr_ret_cnt = user_information["retweet_count"]

    # 更新前の平均を取得
    pre_fav_average = 0 if usr_tweet_cnt == 0 else user_information[
        "favorite_count"] / usr_tweet_cnt
    pre_rt_average = 0 if usr_tweet_cnt == 0 else user_information[
        "retweet_count"] / usr_tweet_cnt

    # 分散を更新するのに必要な情報を更新
    user_information["favorite_count"] += tweet_fav_count
    user_information["retweet_count"] += tweet_rt_count

    # いいねの分散を更新
    user_information["favorite_var"] = get_var_by_pre_var(
        usr_tweet_cnt, user_information["favorite_var"], pre_fav_average,
        user_information["favorite_count"] / (usr_tweet_cnt + 1), tweet_fav_count)

    # RTの分散を更新
    user_information["retweet_var"] = get_var_by_pre_var(
        usr_tweet_cnt, user_information["retweet_var"], pre_rt_average,
        user_information["retweet_count"] / (usr_tweet_cnt + 1), tweet_rt_count)
    # ツイート数を更新
    user_information["tweet_count"] += 1

    return user_information


def get_var_by_pre_var(n, pre_var, pre_ave, new_ave, data):
    return (n * (pre_var + pow(pre_ave, 2)) + pow(data, 2)) / (n+1) - pow(new_ave, 2)
