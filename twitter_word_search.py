
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import common
import re
import datetime

def output_see(search_word,user,min_fav,from_date,to_date,limit):
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
    #Twitterでスクレイピングを行い特定キーワードの情報を取得 
    for tweet in sntwitter.TwitterSearchScraper(condition).get_items():
        if len(tweet_data) == limit:
            break
        medias = []
        # メディア取得
        if tweet.media != None:
            # print(tweet.media)
            for media in tweet.media:
                # print(media)
                # 動画の場合
                if type(media) is sntwitter.Video or type(media) is sntwitter.Gif:
                    thumbnailUrl = media.thumbnailUrl
                    # print(media['variants'])
                    # 最高画質の動画のビットレートを特定
                    max_bit = max([int(dct.bitrate or 0) for dct in media.variants])
                    # 最高画質の動画を格納
                    for variant in media.variants:
                        if variant.bitrate == max_bit:
                            medias.append(['video',variant.url,thumbnailUrl])
                            break
                # 画像の場合
                else:
                    medias.append(['img',media.fullUrl,media.previewUrl])
        viewCount = int(tweet.viewCount or 0)
        tweet_data.append([len(tweet_data), #連番
        common.change_time(tweet.date), #日時
        tweet.rawContent.replace('\n','<br>'), #テキスト
        str(tweet.user.displayname), #ツイート主
        tweet.url,
        tweet.likeCount, #いいね
        tweet.retweetCount, #RT
        int(tweet.viewCount or 0),
        str(0 if viewCount == 0 else round(tweet.likeCount / viewCount * 100, 3)) + '%',
        # int(tweet.viewCount or "0"), #いんぷれっしょン
        # int(tweet.viewCount or None), #いんぷれっしょン
        medias
        ])
    print('yomikan')
    sorce = ''
    
    for tweets in tweet_data:
        # print(tweets)
        sorce += '<tr>'
        for tweet in tweets:
            sorce += '<td>'
            if type(tweet) is list:
                for image in tweet:
                    if image[0] == 'video':
                        # print('video')
                        video = image[1]
                        thumbnailUrl = image[2]
                        sorce += (f'<a href="{video}" target="_blank">   ')
                        sorce += (f'<video src="{video}" poster="{thumbnailUrl}" height="100">   ')
                        sorce += ('</a>')
                    else:
                        # print('image')
                        image = image[1]
                        thumbnailUrl = image[2]
                        sorce += (f'<a href="{image}" target="_blank">   ')
                        sorce += (f'<img src="{image}" height="100">   ')
                        sorce += ('</a>')
            # コメントアウト中Twitter表示
            # elif "https://twitter.com/" in str(tweet):
            #     sorce += ('<blockquote class="twitter-tweet">')
            #     sorce += (f'<a href="{tweet}"></a>')
            #     sorce += ('</blockquote>')
            else:
                sorce += (str(tweet))
            sorce += '</td>'
        sorce += '</tr>'
    sorce += '</table>'
    print(datetime.datetime.now())
    return sorce