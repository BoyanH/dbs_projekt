#!/bin/python3.6
from flask import Flask
from flask import send_from_directory
from cleaner import cleanData
from DBController import DBController
from TableParser import TableParser
from Cluster import Cluster
import HashtagTimeline
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5234))
host = '0.0.0.0'

@app.route('/')
def index():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'client'), 'index.html')

@app.route('/clustering')
def clustering():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'client'), 'index.html')

@app.route('/timeline')
def timeline():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'client'), 'index.html')

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

@app.route('/public/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'client'), filename)


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


    app.secret_key = 'abrakadabra'
    app.run(host=host, port=port)
