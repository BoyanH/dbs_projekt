import csv
from DBController import DBController
from Extractor import Extractor
from Utils import Utils
from Contract import Contract

class TableParser:

	filepath = 'test.csv'
	csvfile = open(filepath, 'r', encoding='cp1252')
	csv_reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

	@staticmethod
	def getTweetFromEntry(entry):

		return {

			Contract.ADD_TO_TABLE_KEY: 'tweet',
			'id': Utils.getRandom8ByteInt(),
			'author': entry['handle'],
			'text': entry['text'],
			'time': Extractor.extractTime(entry),
			'rating': Extractor.calculateRatingForTweet(entry)  
		}

	@staticmethod	
	def getHashTagsFromHTTexts(hashtagTexts):
		hashtags = []

		for ht in hashtagTexts:
			hashtags.append(
				{
					Contract.ADD_TO_TABLE_KEY: 'hashtag',
					'textlowercase': ht
				}
			)
		
		return hashtags

	@staticmethod	
	def getWeekFromEntry(entry):
		return {
			Contract.ADD_TO_TABLE_KEY: 'week',
			'startdate': Extractor.getWeekStart(entry),
			'enddate': Extractor.getWeekEnd(entry)
		}

	@staticmethod
	def getUsedIns(week, hashtags):
		
		usedIns = []
		startDate = week['startdate']

		for ht in hashtags:
			usedIns.append(
				{
					Contract.ADD_TO_TABLE_KEY: 'usedin',
					'hashtagtext': ht,
					'weekstartdate': startDate,
					'count': 1
				}
			)

		return usedIns


	@staticmethod
	def getPostedIn(week, tweet):
		return {
			Contract.ADD_TO_TABLE_KEY: 'postedin',
			'tweetid': tweet['id'],
			'weekstartdate': week['startdate']
		}

	@staticmethod
	def getContains(tweet, hashtags):
		
		contains = []
		tweetid = tweet['id']

		for ht in hashtags:
			contains.append(
				{
					Contract.ADD_TO_TABLE_KEY: 'contains',
					'hashtagtext': ht,
					'tweetid': tweetid
				}
			)

		return contains

	@staticmethod
	def getUsedTogetherWithFromHTTexts(hashtagTexts):
		
		pairs = Utils.getUniquePairs(hashtagTexts)
		usedTogetherWiths = []

		for pair in pairs:
			usedTogetherWiths.append(
				{
					Contract.ADD_TO_TABLE_KEY: 'usedtogetherwith',
					'primaryhashtag': pair[0],
					'togetherwithhashtag': pair[1],
					'count': 1
				}
			)

		return usedTogetherWiths

	@staticmethod
	def parseRow(row, dbController):

		hashtagTexts = Extractor.extractHashtags(row)

		tweet = TableParser.getTweetFromEntry(row)
		week = TableParser.getWeekFromEntry(row)
		hashtags = TableParser.getHashTagsFromHTTexts(hashtagTexts)

		usedIns = TableParser.getUsedIns(week, hashtagTexts)
		postedIn = TableParser.getPostedIn(week, tweet)
		contains = TableParser.getContains(tweet, hashtagTexts)
		usedTogetherWiths = TableParser.getUsedTogetherWithFromHTTexts(hashtagTexts)

		dbController.addMultiple(tweet, week, hashtags, usedIns, postedIn, contains, usedTogetherWiths)

	@staticmethod
	def parseTables():
		dbController = DBController()

		for row in TableParser.csv_reader:
		    TableParser.parseRow(row, dbController)

		dbController.close()

TableParser.parseTables()


