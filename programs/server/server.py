#!/bin/python3.6
from flask import Flask
from flask import send_from_directory
from cleaner import cleanData
from DBController import DBController
from TableParser import TableParser
from Cluster import Cluster
import HashtagTimeline
import os
import json
import datetime

app = Flask(__name__)
port = int(os.environ.get("PORT", 5234))
host = '0.0.0.0'

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)

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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(dir_path, '../client'), filename)

@app.route('/api/clusterData')
@app.route('/api/clusterData/<hashtag>')
def clustersJSON(hashtag=None):
    return Cluster.fromDBtoJSON(hashtag=hashtag)

@app.route('/api/authors')
def getAuthors():
    authors = dbController.getAuthors()
    print(authors)
    return json.dumps({

            "authors": authors

        }, indent = 4)

@app.route('/api/tweet')
@app.route('/api/tweet/<author>')
def getTweets(author = None):

    tweets = dbController.getTweets(author)
    return json.dumps({

            "tweets": tweets

        }, indent = 4, default=date_handler)

@app.route('/api/hashtagsByTweet/<tweetId>')
def getHashtagsByTweet(tweetId):
    hashtags = dbController.getHashtagsByTweet(tweetId)

    return json.dumps({

            "hashtags": hashtags

        }, indent = 4)

@app.route('/api/getTopHashtags')
def getTopHashtags():
    hashtags = dbController.getTopHashtags()

    return json.dumps({

            "hashtags": hashtags

        }, indent = 4)

@app.route('/api/searchHashtags/<hashtagText>')
def searchHashtags(hashtagText):
    hashtags = dbController.getHashtagsByText(hashtagText);

    return json.dumps({

            "hashtags": hashtags if hashtags != None else []

        }, indent = 4)

@app.errorhandler(404)
def index(err):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(dir_path, '../client'), 'index.html')

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
