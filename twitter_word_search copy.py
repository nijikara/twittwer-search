import tweepy
import common
import datetime

def output_see(search_word):
    
    # # 認証　
    # api_key = 'fVH9Fv8KPWHvBAH4Mw7tobhhn'
    # api_key_secret = 'MB1gwWuCZRobl8LjWcoaxtjXkGiA60uxEtleLTPh7GrECMrhBl'
    # access_token = '2801208301-gKlwvi3vbtgKQ30zl6QuiDSN4Xh9QJHCyk8YJas'
    # access_token_secret = 'lhNgSVOi7OKy5o0ml1Ll5CTLMCmkNSVMt81nJA7XoM8RW'
    # bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKUSkwEAAAAACCzscXnfQgL8VdJTaJqF%2FVYuXhA%3DiNBYSQLNImqKDdvolwxcGFs6EUpdn3LgCOGJUEvwIHlLueyrWM'

    # client = tweepy.Client(
    #     consumer_key=api_key,
    #     consumer_secret=api_key_secret,
    #     access_token=access_token,
    #     access_token_secret=access_token_secret,
    #     bearer_token=bearer_token
    # )


    # 最新のツイートを取得
    # tweets = client.search_recent_tweets(query='軍師ミノル',  # 検索ワード
    #                                     max_results=10,  # 取得件数
    #                                     tweet_mode='extended',  # 省略されたリンクを全て取得
    #                                     include_entities=True,  #  # 省略されたツイートを全て取得
    #                                     )

    # # 各種ツイッターのキーをセット
    consumer_key = '5Xwmm187IlTaS3lLLoGWLP6Jk'
    consumer_secret = 'QcqV6fAODTmpBJplPY3UsPecaz6X14PsiJvk1iYzJI6KxvVpZC'
    access_key = '2801208301-YYTY5gtgU9311ckKtBS5NwXl5WSiLTjIRaYHbxC'
    access_secret = 'BRjAgo373jFGXY5DKrYyFDyqoJvsmhEVv1pB7WieYaiTj'

        # # 各種ツイッターのキーをセット( Tweets: Full Archive / Sandbox)
    # consumer_key = 'M228EDjlPGt8ili3bfP0btwNF'
    # consumer_secret = 'O7UUwyVCru4qZ50m2bsyrCbXyYhN1MuGHTHjRZchQOhDx9a8sB'
    # access_key = '2801208301-CBqu0LC1nf49XjMyzu0eBAlTU1wKfi9GqbnMHcI'
    # access_secret = 'JulXQCRvi6WzhqW4cdHVav6awQePImUUYoX0qvtQH3Ewk'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #ツイート取得
    tweet_data = []
    idx = 0
        # for tweet in tweepy.Cursor(
        # api.user_timeline,
        # screen_name = screen_name,
        # exclude_replies = False,
        # # include_rts = False,
        # tweet_mode="extended").items():
    dt_now = datetime.datetime.now()
    #1時間前を取得したいので、hours=-1。もし1日前だったらdays=-1
    dt_now = dt_now + datetime.timedelta(hours=0)
    dt_now2 = dt_now + datetime.timedelta(days=-120)

    now = dt_now.strftime('%Y-%m-%d_%H:%M:%S_JST')
    before = dt_now2.strftime('%Y-%m-%d_%H:%M:%S_JST')
    search_word += ' exclude:retweets'
    print(search_word)
    tweets = tweepy.Cursor(api.search_tweets,
                        q=search_word,  # 検索ワード
                        tweet_mode='extended',  # 省略されたリンクを全て取得
                        include_entities=True,  #  # 省略されたツイートを全て取得
                        since_id=before,
                        until=now,
                        result_type='mixed',  # 最新のツイートを検索
                        lang='ja'  # 検索対象の言語
                        ).items(1000)  # 取得件数

    for tweet in tweets:
        print(tweet.created_at)
        print(tweet.full_text.replace('\n','<br>'))
        print(tweet.favorite_count)
        print(tweet.retweet_count)
        print(tweet.user.screen_name)
        idx += 1
        tweet_data.append([idx, #連番
        common.change_time(tweet.created_at), #日時
        tweet.full_text.replace('\n','<br>'), #テキスト
        str(tweet.user.name), #ツイート主
        "https://twitter.com/" + str(tweet.user.screen_name) + "/status/" + str(tweet.id),
        tweet.favorite_count, #いいね
        tweet.retweet_count #RT
        # media_url #画像
         ])

        print(tweet)
        # RTを除外
        # if "RT @" in tweet.full_text[0:4]:
        #     continue
        # media_url = []
        # idx += 1
        # if 'media' in tweet.entities:
        #     for media in tweet.extended_entities['media']:
        #         # print(media)
        #         media_url.append(media['media_url'])
        #         if 'video_info' in media:
        #             for video in media['video_info']['variants']:
        #                 # print(video['url'])
        #                 media_url.append(video['url'])

        # tweet_data.append([idx, #連番
        # common.change_time(tweet.created_at), #日時
        # tweet.full_text.replace('\n','<br>'), #テキスト
        # "https://twitter.com/" + screen_name + "/status/" + str(tweet.id),
        # tweet.favorite_count, #いいね
        # tweet.retweet_count, #RT
        # media_url #画像
        #  ])

    sorce = ''
    
    for tweets in tweet_data:
        # print(tweets)
        sorce += '<tr>'
        for tweet in tweets:
            sorce += '<td>'
            if type(tweet) is list:
                for image in tweet:
                    if not 'm3u8' in image:
                        if 'mp4' in image:
                            sorce += (f'<a href="{image}" target="_blank">   ')
                            sorce += (f'<video src="{image}" height="100">   ')
                            sorce += ('</a>')
                        else:
                            sorce += (f'<a href="{image}" target="_blank">   ')
                            sorce += (f'<img src="{image}" height="100">   ')
                            sorce += ('</a>')

            # elif "https://twitter.com/" in tweet:
            #     sorce += (f'<a href="{tweet}">')
            else:
                sorce += (str(tweet))
            sorce += '</td>'
        sorce += '</tr>'
    sorce += '</table>'
    return sorce