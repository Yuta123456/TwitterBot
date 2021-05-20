import oseti

analyzer = oseti.Analyzer()

# いつもに比べて人気のツイートかどうか？


def is_popular_tweet(tweet, user_information):
    fav_var = user_information["favorite_var"]
    rt_var = user_information["retweet_var"]
    fav_ave = 0 if user_information["tweet_count"] == 0 else user_information["favorite_count"] / \
        user_information["tweet_count"]
    rt_ave = 0 if user_information["tweet_count"] == 0 else user_information["retweet_count"] / \
        user_information["tweet_count"]
    # いつもより若干伸びているようなら人気のツイートと判定
    if (tweet.favorite_count > fav_ave + pow(fav_var, 0.5) and tweet.retweet_count >= int(rt_ave + pow(rt_var, 0.5))):
        return True
    return False

# 人の悪口を言っているかどうか？


def is_bad_word_for_people(tweet, user_information):
    text = tweet.text
    is_negative_tweet = False
    try:
        analyze_result = analyzer.analyze(text)
    except:
        print("Tweetの解析に失敗しました。")
        return False
    print("結果:{} 文章:{}".format(analyze_result, text))
    if ((sum(analyze_result) / len(analyze_result)) <= -0.9):
        is_negative_tweet = True
    # 人気かつネガティブなら人の悪口と判断
    return is_negative_tweet and is_popular_tweet(tweet, user_information)

#  データが平均から標準偏差の値の3倍以上離れていたら、外れ値と判断する


def is_outliers(tweet, user_information):
    fav_var = user_information["favorite_var"]
    rt_var = user_information["retweet_var"]
    fav_ave = 0 if user_information["tweet_count"] == 0 else user_information["favorite_count"] / \
        user_information["tweet_count"]
    rt_ave = 0 if user_information["tweet_count"] == 0 else user_information["retweet_count"] / \
        user_information["tweet_count"]
    return (tweet.favorite_count > fav_ave + 3 * pow(fav_var, 0.5)) and tweet.retweet_count > rt_ave + 3 * pow(rt_var, 0.5)
# ポジティブなことを言っているかどうか？


def is_positive_word(tweet):
    text = tweet.text
    analyze_result = analyzer.analyze(text)
    if ((sum(analyze_result) / len(analyze_result)) >= 0.9):
        return True
    return False
