from DBController import DBController
import numpy as np

class Cluster:

	def __init__(self):
		self.dBController = DBController();
		self.hashtagTexts = self.dBController.getHashtagTexts()
		self.dayDates = self.dBController.getDayDates()

		hashtagDimensionMapper = {}
		dayDimensionMapper = {}
		counter = 0

		for text in self.hashtagTexts:
			hashtagDimensionMapper[text] = counter
			counter += 1

		for date in self.dayDates:
			dayDimensionMapper[date] = counter
			counter += 1 

		self.hashtagDimensionMapper = hashtagDimensionMapper
		self.dayDimensionMapper = dayDimensionMapper
		self.dimensions = counter

	def calculateClusters(self):
		self.updateHashtagVectors()

	def updateHashtagVectors(self):
		htVectors = {}

		# initialize vectors of each hashtag
		for ht in self.hashtagTexts:
			htVectors[ht] = [0] * self.dimensions

		for ht in self.hashtagTexts:

			dates = self.dBController.getDayDatesForHashtag(ht)
			pairs = self.dBController.getUsedTogetherWithPairsForHashtag(ht)

			for date in dates:
				dimensionForDate = self.dayDimensionMapper[date]
				htVectors[ht][dimensionForDate] += 1

			# add count of usedTogetherWith to the 2 dimensions of a vector corresponding to the 2 hashtag texts
			for pair in pairs:

				for i in range(2):
					dimensionForHt = self.hashtagDimensionMapper[pair[i]]
					htVectors[ht][dimensionForHt] += pair[2] #pair[2] = count

		for ht in htVectors:
			self.dBController.updateHashtagVector(ht, htVectors[ht]);

		self.dBController.connection.commit();
