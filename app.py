from flask import Flask, render_template
from flask import request
import datetime
# import twitter_word_search_0209 as twitter_word_search
# import twitter_word_search_0208 as twitter_word_search
import twitter_word_search as twitter_word_search
# import twitter_word_search_0210 as twitter_word_search

from flask import Markup
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('layout.html', title='twitter_get')

# ↓ /scrapingをGETメソッドで受け取った時の処理
@app.route('/scraping', methods=['GET', 'POST'])
def get():
    # 現在時刻　デバッグ確認用
    print(datetime.datetime.now())
    now = datetime.datetime.now()
    today = datetime.date.today()
    user = request.args.get("user","")
    word = request.args.get("word","")
    ignore = request.args.get("ignore","")
    fav = request.args.get("fav","")
    max_record = int(request.args.get("max-record",""))
    time_span = request.args.get("radio")
    from_date = ''
    # パラメータ確認
    print(request.args)
    # 日付の開始位置指定
    if time_span[0] == 'y':
        from_date = today  - relativedelta(years=int(time_span[1]))
    elif time_span[0] == 'm':
        from_date = today  - relativedelta(months=int(time_span[1]))
    to_date = today
    print(to_date)
    # 検索
    sorce = twitter_word_search.output_see(word,user,fav,from_date,to_date,max_record,ignore)
    if request.method == 'GET': # GETされたとき
        print('出力')
        sorce = Markup(sorce)
        end = datetime.datetime.now()
        # return render_template('template.html',sorce = sorce)
        return render_template('template.html',sorce = sorce, now = now, end = end)
        
    elif request.method == 'POST': # POSTされたとき
        return 'POST'


if __name__ == "__main__":
    app.run(debug=True)