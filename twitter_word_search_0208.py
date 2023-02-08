
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import common
import re
import datetime

def output_see(search_word,user,min_fav,from_date,to_date,limit):
    print("0208")
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
    #Twitterでスクレイピングを行い特定キーワードの情報を取得 
    scraped_tweets = sntwitter.TwitterSearchScraper(condition).get_items()
    # scraped_tweets = sntwitter.TwitterSearchScraper(str(search) + f' since:{from_date} until:{to_date} ').get_items()

    #最初の10ツイートだけを取得し格納
    sliced_scraped_tweets = itertools.islice(scraped_tweets, limit)
    #データフレームに変換する(欠損部は0にする)
    df = pd.DataFrame(sliced_scraped_tweets).fillna(0)

    print('yomikan')
    sorce = ''

    print(datetime.datetime.now())
    return sorce