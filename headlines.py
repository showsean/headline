# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask,render_template
import feedparser
app=Flask(__name__)

FEED = {'qq':"http://news.qq.com/newsgn/rss_newsgn.xml",
        'baidu':'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss',
        'rm':'http://www.people.com.cn/rss/politics.xml',
        'sina':'http://rss.sina.com.cn/news/china/focus15.xml',
        'zhihu':"http://www.zhihujingxuan.com/rss",
        '36':"http://36kr.com/feed"}
@app.route("/")
@app.route('/<publication>')
def get_news(publication='qq'):
    if publication not in FEED:
        publication='sina'
    feed = feedparser.parse(FEED[publication])
    return render_template("home.html",articles=feed['entries'])

if __name__=="__main__":
    app.run(port=5000,debug=True)

