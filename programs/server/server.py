#!/bin/python3.6
from flask import Flask
from cleaner import cleanData
from DBController import DBController
from TableParser import TableParser
from Cluster import Cluster
import HashtagTimeline

app = Flask(__name__)
port = 5234
host = '127.0.0.1'

@app.route('/')
def index():
    return 'Hello world'

@app.route('/topTweets')
def getTopTweets():
    topTweets = dbController.getTopTweets()
    return 'Top tweets: <br><br>' + '<br><br>'.join(str(e) for e in topTweets)

@app.route('/hashtag/daily')
@app.route('/hashtag/daily/<hashtag>')
def getDaily(hashtag=None):
    if not hashtag or hashtag == '':
        return HashtagTimeline.dailyTotalHashtags()
    else:
        return HashtagTimeline.dailyHashtag(hashtag)

@app.route('/hashtag/weekly')
@app.route('/hashtag/weekly/<hashtag>')
def getWeekly(hashtag=None):
    if not hashtag or hashtag == '':
        return HashtagTimeline.weeklyTotalHashtags()
    else:
        return HashtagTimeline.weeklyHashtag(hashtag)

if __name__ == '__main__':

    dbController = DBController()
    filled = dbController.checkFilled()
    dbController.close();

    if not filled:
        cleanData()
        TableParser.parseTables()
        Cluster().calculateClusters()
    else:
        print('Data already imported :)')


    app.run(host=host, port=port)
