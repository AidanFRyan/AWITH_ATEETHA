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
    for i in reddit.subreddit('hardwareswap').hot(limit=10):
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
            print(tagTitle)

            tagged = nltk.pos_tag(nltk.word_tokenize(i.selftext))
            tags = [t for w,t in tagged]
            dLoc = tags.index('$')
            price = tagged[dLoc+1]
            l = dLoc
            while 'NNP' not in [t for w,t in tagged[l:dLoc]] and l >= 0:
                l -= 1
            print(tagged[l:dLoc])
            print(price)