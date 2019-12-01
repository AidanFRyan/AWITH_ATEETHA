import praw
import re
import datetime
import numpy
# import plotly.offline as plot
# import plotly.graph_objects as graph
import nltk
import mysql.connector as sql

def splitString(i):
    retval = []
    prev = 0
    for l in range(len(i)):
        if l > 0:
            if i[l].isalpha() != i[l-1].isalpha() or i[l].isdigit() != i[l-1].isdigit():
                retval.append(i[prev:l])
                prev = l
    retval.append(i[prev:len(i)])
    return retval

def furtherSplit(p):
    t = []
    for i in p:
        for l in splitString(i):
            t.append(l)
    return t

def trimPrice(p):
    s = ''
    for i in p:
        if i.isdigit() or i == '.':
            s = s + i
        elif i == ',':
            continue
        else:
            break
    return s

def isPrice(p):
    if p.isdigit():
        return True
    if p == '':
        return False
    for i in p:
        if not i.isdigit() and i != '.':
            return False
    return True
add_query = ("INSERT IGNORE INTO Queries (qstr, postID, price) VALUES (%s, %s, %s)")
add_post = ("INSERT IGNORE INTO Posts (id, title, date, username, url) VALUES (%s, %s, %s, %s, %s)")
class Searcher():
    reddit = praw.Reddit(client_id='Q0cB-L4Ukm4a7g', client_secret='jjkxJyXsyqWbqUnwRu3nsw054t0', user_agent='thejankisinfinite', password='Guitarshredder1')
    db = sql.connect(host='localhost', user='pi', passwd='pi', database='tbase')
    cx = db.cursor()
    hw = reddit.subreddit('hardwareswap')
    def getHot(self, limit=100):
        for i in self.hw.hot(limit=limit):
            if i.link_flair_text == "SELLING" and '$' in i.selftext:
                title = i.title.split()[1:]
                s = ' '
                title = s.join(title)
                while("[H]" in title):
                    title = title[1:]
                title = title[2:]
                while("[W]" in title):
                    title = title[:-1]
                title = title[:-2]
                tagTitle = nltk.pos_tag(nltk.word_tokenize(title))
                # print(tagTitle)
                sents = nltk.sent_tokenize(i.selftext)
                words = [nltk.word_tokenize(s) for s in sents]
                ts = [nltk.pos_tag(word) for word in words]
                for tagged in ts:
                    tags = [t for w,t in tagged]
                    while '$' in tags:
                        dLoc = tags.index('$')
                        price = tagged[dLoc+1]
                        tags = tags[dLoc+1:]
                        if price[1] != "CD" or not price[0].isdigit():
                            continue
                        print([w for w,t in tagTitle])
                        # print([w for w,t in tagged[:dLoc]])
                        print(tagged[:dLoc])
                        # print(s.join([w for w,t in tagged[l:dLoc]]))
                        print("$" + str(price[0]))
    def queryDatabase(self, qw):
        posts = []
        pids = []
        out = []
        for i in qw:
            self.cx.execute("SELECT DISTINCT * FROM Queries WHERE qstr = \"" + i + '"')
            for (q, pid, price) in self.cx:
                if pid not in pids:
                    posts.append({'pid': pid, 'price': price})
                    pids.append(pid)
        print(posts)
        for pid in posts:
            self.cx.execute("SELECT DISTINCT * FROM Posts WHERE id = \"" + pid['pid'] + '"')
            for (id, title, date, username, url) in self.cx:
                out.append({'price': pid['price'], 'link': url, 'title': title, 'username': username})
        return out
        
    def searchFor(self, query=''):
        lst = []
        qw = furtherSplit(nltk.word_tokenize(query))
        for i in self.hw.search(query=query):
            if '$' in i.selftext:
                if i.link_flair_text == 'SELLING' and set([w.lower() for w in qw]).issubset(set([w.lower() for w in furtherSplit(nltk.word_tokenize(i.title))])):
                    wors = furtherSplit(nltk.word_tokenize(i.selftext))
                    sents = nltk.pos_tag(wors)
                    if len([t for w,t in sents if t == '$']) >= 1:
                        prices = []
                        curPrice = 0
                        words = [w for w,t in sents]
                        subWords = words
                        while '$' in subWords:
                            pos = subWords.index('$')
                            price = subWords[pos+1]
                            if isPrice(trimPrice(price)):
                                prices.append((pos + (len(words) - len(subWords)), trimPrice(price)))
                            else:
                                print('bad price ' + trimPrice(price))
                            subWords = subWords[pos+1:]
                        if len(prices) > 1:
                            prevPos = 0
                            for p in prices:
                                if set([w.lower() for w in qw]).issubset(set([w.lower() for w,t in sents[prevPos:p[0]]])):
                                    curPrice = p[1]
                                    break
                                prevPos = p[0]
                            if curPrice == 0:
                                prevPos = len(sents)
                                prices.reverse()
                                for p in prices:
                                    if set([w.lower() for w in qw]).issubset(set([w.lower() for w,t in sents[p[0]:prevPos]])):
                                        curPrice = p[1]
                                        break
                                    prevPos = p[0]
                            if curPrice == 0:
                                curPrice = prices[0][1] #dumb way of avoiding price of 0, assume its the first one if not found yet
                        elif len(prices) == 1:
                            curPrice = prices[0][1]
                        else:
                            continue
                        lst.append({'id': i.id, 'title': i.title, 'link': 'http://www.reddit.com'+i.permalink, 'date': i.created_utc, 'query_words': qw, 'price': curPrice, 'username': i.author.name})
        for i in qw:
            for l in lst:
                self.cx.execute(add_query, (i.lower(), l['id'], l['price']))
        for l in lst:
            self.cx.execute(add_post, (l['id'], l['title'], l['date'], l['username'], l['link']))
        self.cx.execute("commit")
        return self.queryDatabase([w.lower() for w in qw])
        # return lst