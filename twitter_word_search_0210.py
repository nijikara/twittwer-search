
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import common
import re
import datetime

def output_see(search_word,user,min_fav,from_date,to_date,limit):
    start = datetime.datetime.now()
    # condition = 'lang:ja '
    condition = ''
    # 最低いいね数
    if min_fav != '':
        condition = f'min_faves:{min_fav} '
    # 検索日From
    if from_date != '':
        condition += f'since:{from_date} '
    # デバッグ用
    # condition += f'since:2022-12-19_12:23:00_JST '
    # condition += f'until:2022-12-19_12:28:00_JST '
    # 検索ワード
    if search_word != '':
        # AND条件用処理
        for word in re.split('\s', search_word):
            condition += f'"{word}" '
        condition += 'OR @i -@i '
    # 検索ユーザー
    if user != '':
        condition += f'from:{user} '
    else:
        condition += 'lang:ja '
    # condition += 'filter:videos '
    # print(user)
    print(condition)
    tweet_data = []
    count = 0
    #Twitterでスクレイピングを行い特定キーワードの情報を取得 
    # ツイートを取得
    for tweet in sntwitter.TwitterTweetScraper(1606852115535900673).get_items():
    # ハッシュタグで検索取得
    # for tweet in sntwitter.TwitterHashtagScraper('ミノル').get_items():
        # トレンド取得
    # for tweet in sntwitter.TwitterTrendsScraper().get_items():
        print(tweet)
    print('yomikan')
    sorce = ''

    sorce += f'{start}'
    sorce += '<br>'
    sorce += f'{datetime.datetime.now()}'
    print(datetime.datetime.now())
    return sorce