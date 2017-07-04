from flask import Flask
from cleaner import cleanData
from DBController import DBController
from TableParser import TableParser
from Cluster import Cluster

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
