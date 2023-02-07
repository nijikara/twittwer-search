import tweepy
import common
import datetime
from requests_oauthlib import OAuth1Session
import json

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
    # consumer_key = '5Xwmm187IlTaS3lLLoGWLP6Jk'
    # consumer_secret = 'QcqV6fAODTmpBJplPY3UsPecaz6X14PsiJvk1iYzJI6KxvVpZC'
    # access_key = '2801208301-YYTY5gtgU9311ckKtBS5NwXl5WSiLTjIRaYHbxC'
    # access_secret = 'BRjAgo373jFGXY5DKrYyFDyqoJvsmhEVv1pB7WieYaiTj'

    # # 各種ツイッターのキーをセット( Tweets: Full Archive / Sandbox)
    consumer_key = 'M228EDjlPGt8ili3bfP0btwNF'
    consumer_secret = 'O7UUwyVCru4qZ50m2bsyrCbXyYhN1MuGHTHjRZchQOhDx9a8sB'
    access_key = '2801208301-CBqu0LC1nf49XjMyzu0eBAlTU1wKfi9GqbnMHcI'
    access_secret = 'JulXQCRvi6WzhqW4cdHVav6awQePImUUYoX0qvtQH3Ewk'

    twitter = OAuth1Session(consumer_key, consumer_secret, access_key, access_secret)
    # Twitter Endpoint(検索結果を取得する)
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/getTwitter2023.json'

    # Enedpointへ渡すパラメーター
    keyword = '"ピクミン"'

    params ={
            'query' : keyword ,  # 検索キーワード
            'maxResults': 1000 ,   # 取得するtweet数
            'fromDate' : 201301311500 ,
            'toDate' : 201302011500 
            }

    req = twitter.get(url, params = params)
    print('*************unti******************************')
    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res['results']:
            print(line['text'])
            print('*******************************************')
    else:
        print("Failed: %d" % req.status_code)
    return keyword
    