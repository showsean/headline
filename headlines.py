# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask,render_template,request
import feedparser
app=Flask(__name__)

FEED = {'qq':"http://news.qq.com/newsgn/rss_newsgn.xml",
        'rm':'http://www.people.com.cn/rss/politics.xml',
        'sina':'http://rss.sina.com.cn/news/china/focus15.xml',
        'yueguang':'http://feed.williamlong.info/'}
@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in FEED:
        publication = "qq"
    else:
        publication = query.lower()
    feed = feedparser.parse(FEED[publication])
    return render_template("home.html",articles=feed['entries'])

if __name__=="__main__":
    app.run(port=5000,debug=True)

