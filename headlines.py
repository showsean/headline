# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
import feedparser
app=Flask(__name__)

FEED = {'qq':"http://news.qq.com/newsgn/rss_newsgn.xml",
        'baidu':'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss',
        'rm':'http://www.people.com.cn/rss/politics.xml',
        'sina':'http://rss.sina.com.cn/news/china/focus15.xml'
       }
@app.route("/")
@app.route('/<publication>')
def get_news(publication='qq'):
    if publication not in FEED:
        publication='sina'
    feed = feedparser.parse(FEED[publication])
    news = feed['entries'][0]
    return """<html>
<body>
<h1>新闻</h1>
<b>{0}</b><br/>
<i>{1}</i><br/>
<p>{2}</p><br/>
</body>
</html>""".format(news.get("title"),news.get("published"),news.get("summary"))

if __name__=="__main__":
    app.run(port=5000,debug=True)

