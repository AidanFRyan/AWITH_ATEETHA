import praw
import re
import datetime
import numpy
import plotly.offline as plot
import plotly.graph_objects as graph
import nltk
import mysql.connector as sql
db = sql.connect(host='localhost', user='pi', passwd='pi', database='testbase')

reddit = praw.Reddit(client_id='Q0cB-L4Ukm4a7g', client_secret='jjkxJyXsyqWbqUnwRu3nsw054t0', user_agent='thejankisinfinite', password='Guitarshredder1')

with open("output.txt", "w") as file:
    for i in reddit.subreddit('hardwareswap').hot(limit=100):
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