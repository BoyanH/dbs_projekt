import time
from datetime import datetime
import re

class Extractor:

	RATING_WEIGHT = {
		"retweetCount": 0.8,
		"favouriteCount": 1.2
	}

	TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
	
	@staticmethod
	def calculateRatingForTweet(entry):
		retweetCount = float(entry['retweet_count'])
		favouriteCount = float(entry['retweet_count'])

		return retweetCount*Extractor.RATING_WEIGHT['retweetCount'] + retweetCount*Extractor.RATING_WEIGHT['favouriteCount']

	@staticmethod
	def extractTime(entry):
		time = entry['time']

		return datetime.strptime(time, Extractor.TIME_FORMAT)

	@staticmethod
	def getNthDayOfWeek(entry, n):
		time = Extractor.extractTime(entry)
		isoCalender = time.date().isocalendar()

		return datetime.strptime('{0} {1} {2}'.format(isoCalender[0], isoCalender[1], n), '%G %V %u').date()

	@staticmethod
	def getWeekStart(entry):
		return Extractor.getNthDayOfWeek(entry, 1)

	@staticmethod
	def getWeekEnd(entry):
		return Extractor.getNthDayOfWeek(entry, 7)

	@staticmethod
	def extractHashtags(entry):
		text = entry['text']
		searchedUntil = 0
		hashtags = []

		try:
			while (True):

				crntHashtagStart = text.index('#', searchedUntil) + 1

				try:
					crntHashtagEnd = re.search('[^a-zA-Z0-9]', text[(crntHashtagStart):]).start() + crntHashtagStart
				except AttributeError as atrErr:
					crntHashtagEnd = len(text)

				crntHashtag = text[crntHashtagStart:crntHashtagEnd].lower()
				searchedUntil = crntHashtagEnd

				if not crntHashtag in hashtags:
					hashtags.append(crntHashtag)

		except ValueError as err:
			# no more hashtags found, we are ready
			pass

		return hashtags

