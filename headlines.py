# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask,render_template,request,flash
import feedparser
import json
import urllib
import urllib2

app=Flask(__name__)
app.config.update(dict(SECRET_KEY="dfghjmnbvfdertyujn"))
FEED = {'qq':"http://news.qq.com/newsgn/rss_newsgn.xml",
        'rm':'http://www.people.com.cn/rss/politics.xml',
        'sina':'http://rss.sina.com.cn/news/china/focus15.xml',
        'yueguang':'http://feed.williamlong.info/'}
api_url="https://api.seniverse.com/v3/weather/now.json?key=gz4j3y0rz4jqmpr4&location={}&language=zh-Hans&unit=c"
CURRENCY_URL="https://openexchangerates.org//api/latest.json?app_id=6ce9f26fd62c4c7b967f736b9aa48d97"

DEFAULTS={"publication":"sina",
          "city":"beijing",
          "currency_from":"CNY",
          "currency_to":"USD"
         }
@app.route("/")
def home():
    publication=request.args.get("publication")
    if not publication:
        publication=DEFAULTS["publication"]
    articles=get_news(publication)
    city=request.args.get("city")
    if not city:
        city=DEFAULTS["city"]
    try:
        weather=get_weather(city)
    except Exception:
        flash("请输入正确的城市名")
    currency_from=request.args.get("currency_from")
    if not currency_from :
        currency_from=DEFAULTS["currency_from"]
    currency_to=request.args.get("currency_to")
    if not currency_to:
        currency_to=DEFAULTS["currency_to"]
    rate,currencies=get_rate(currency_from,currency_to)
    return render_template("home.html",articles=articles,weather=weather,
                          currency_to=currency_to,currency_from=currency_from,rate=rate,currencies=sorted(currencies))

def get_news(query):
    if not query or query.lower() not in FEED:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(FEED[publication])
    return feed['entries']
def get_rate(frm,to):
    all_currency=urllib2.urlopen(CURRENCY_URL).read()

    parsed=json.loads(all_currency).get("rates")
    frm_rate=parsed.get(frm.upper())
    to_rate=parsed.get(to.upper())
    return (to_rate/frm_rate,parsed.keys())

def get_weather(query):
    try:
        query=urllib.quote(query)
        url=api_url.format(query)
        data=urllib2.urlopen(url).read()
        parsed=json.loads(data)
        weather=None
        if parsed.get('results'):
            weather={"description":parsed["results"][0]["now"]["text"],
                     "temperature":parsed["results"][0]["now"]["temperature"],
                     "city":parsed["results"][0]["location"]["name"],
                     "country":parsed["results"][0]["location"]["country"]
                    }
            return weather
    except Exception:
        flash("请输入正确的城市拼写")


if __name__=="__main__":
    app.run(port=5000,debug=True)

