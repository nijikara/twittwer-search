
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import common
import re
import datetime

def output_see(search_word,user,min_fav,from_date,to_date,limit,ignore_word,only_jp):
    # condition = 'lang:ja '
    condition = ''
    # 最低いいね数
    if min_fav != '':
        condition = f'min_faves:{min_fav} '
    # 検索日From
    if from_date != '':
        condition += f'since:{from_date} '
    # デバッグ用
    # condition += f'since:2023-02-16_12:23:00_JST '
    # condition += f'until:2022-12-19_12:28:00_JST '
    # 検索ワード
    if search_word != '':
        # AND条件用処理
        for word in re.split('\s', search_word):
            condition += f'"{word}" '
        condition += 'OR @i -@i '
    # 除外ワード
    if ignore_word != '':
        # AND条件用処理
        for word in re.split('\s', ignore_word):
            condition += f'-"{word}" '
    # 検索ユーザー
    if user != '':
        condition += f'from:{user} '
    else:
        if only_jp == 'on':
            condition += 'lang:ja '
    # condition += 'filter:videos '
    # print(user)
    print(condition)
    tweet_data = []
    count = 0
    # ユーザーを指定して検索する場合↓
    # for tweet in sntwitter.TwitterUserScraper('minoru4160').get_items():

    #Twitterでスクレイピングを行い特定キーワードの情報を取得 
    for tweet in sntwitter.TwitterSearchScraper(condition).get_items():
        if count >= limit:
            break
        count += 1
        if count % 100 == 0:
            print(count)
        medias = []
        # 引用ツイート
        if tweet.quotedTweet != None:
            # print(tweet.quotedTweet.content)
            # medias.append(['quot',tweet.quotedTweet.url])
            medias.append(['quot',tweet.quotedTweet.rawContent])
        # # カード
        # if tweet.card != None:
        #     print(tweet.card)
        #     medias.append(['quot',tweet.card.url])
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

        # tweet_data.append([count, #連番
        # common.change_time(tweet.date), #日時
        # tweet.rawContent.replace('\n','<br>'), #テキスト
        # str(tweet.user.displayname), #ツイート主
        # tweet.url,
        # tweet.likeCount, #いいね
        # tweet.retweetCount, #RT
        # tweet.quoteCount, #引用RT
        # viewCount, #インプレッション
        # str(0 if viewCount == 0 else round(tweet.likeCount / viewCount * 100, 3)) + '%',
        # tweet.replyCount, #リプライ数
        # medias
        # ])
        tweet_data.append({'count':count, #連番
        'date':common.change_time(tweet.date), #日時
        'content':tweet.rawContent.replace('\n','<br>'), #テキスト
        # 'content':tweet.rawContent, #テキスト
        'name':str(tweet.user.displayname), #ツイート主
        'url':tweet.url,
        'likeCount':tweet.likeCount, #いいね
        'retweetCount':tweet.retweetCount, #RT
        'quoteCount':tweet.quoteCount, #引用RT
        'viewCount':viewCount, #インプレッション
        'reaction':str(0 if viewCount == 0 else round(tweet.likeCount / viewCount * 100, 3)) + '%',
        'replyCount':tweet.replyCount, #リプライ数
        'medias':medias
        })
    print('yomikan')
    sorce = ''
    return tweet_data
    
    for tweets in tweet_data:
        # print(tweets)
        sorce += '<tr>'
        for tweet in tweets:
            sorce += '<td>'
            # メディア
            if type(tweet) is list:
                for media in tweet:
                    # print(media)
                    if media[0] == 'video':
                        video = media[1]
                        thumbnailUrl = media[2]
                        sorce += (f'<a href="{video}" target="_blank">   ')
                        sorce += (f'<video src="{video}" poster="{thumbnailUrl}" height="100">   ')
                        sorce += ('</a>')
                    elif media[0] == 'img':
                        media = media[1]
                        thumbnailUrl = media[2]
                        sorce += (f'<a href="{media}" target="_blank">   ')
                        sorce += (f'<img src="{media}" height="100">   ')
                        sorce += ('</a>')
                    elif media[0] == 'quot':
                        sorce += ('<blockquote class="twitter-tweet"  data-cards="hidden" data-conversation="none">')
                        sorce += (f'<a href="{media[1]}"></a>')
                        sorce += ('</blockquote>')
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
    # sorce += f'{start}'
    # sorce += '<br>'
    # sorce += f'{datetime.datetime.now()}'
    print(datetime.datetime.now())
    return sorce