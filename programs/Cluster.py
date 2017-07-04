from DBController import DBController
import numpy as np
from random import randint

CLUSTERS_COUNT = 5
IGNORABLE_CLUSTER_MOVE_DISTANCE = 1

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
		self.htVectors = self.updateHashtagVectors()

		for ht in self.htVectors:
			self.dBController.updateHashtagVector(ht, self.htVectors[ht]);

		self.dBController.connection.commit();

		self.clusterCenters = self.getClusterCenters()
		self.clustersForHt = self.executeKMeans()

		for center in self.clusterCenters:
			self.dBController.addClusterCenter(center)

		self.dBController.connection.commit();

		for ht in self.clustersForHt:
			centerId = self.dBController.getClusterCenterId(self.clustersForHt[ht]);
			self.dBController.addHashtagToCluster(ht, centerId)



		self.dBController.connection.commit();


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

		return htVectors;

	def getClusterCenters(self):

		# Pick CLUSTERS_COUNT amount of random hashtags as cluster centers

		clusterCoordinates = []
		hashtagsAsClusterCenters = []

		while len(clusterCoordinates) < CLUSTERS_COUNT:
			ht = self.hashtagTexts[randint(0, len(self.hashtagTexts)-1 )]

			if (not ht in hashtagsAsClusterCenters):
				hashtagsAsClusterCenters.append(ht)
				currentClusterCenter = self.dBController.getCoordinatesOfHashtag(ht)
				clusterCoordinates.append(currentClusterCenter)


		return clusterCoordinates;

	def executeKMeans(self):
		oldCenters = []
		shouldContiune = True

		while shouldContiune:
			clusterForHt = self.updateHashtagsInClusters()
			oldCenters = self.clusterCenters
			self.clusterCenters = Cluster.calculateNewClusterCenters(clusterForHt, self.clusterCenters, self.htVectors)

			shouldContiune = Cluster.getKMeansShouldContinue(oldCenters, self.clusterCenters)

		return clusterForHt


	def updateHashtagsInClusters(self):
		clusterForHt = {}

		for ht in self.htVectors:
			currentCoords = self.htVectors[ht]
			nearestClusterCoord = Cluster.getNearestClusterCoords(currentCoords, self.clusterCenters)
			clusterForHt[ht] = nearestClusterCoord

		return clusterForHt

	@staticmethod
	def getKMeansShouldContinue(oldCenters, newCenters):

		shouldContiune = False
		oldCenters.sort()
		newCenters.sort()

		assert len(oldCenters) == len(newCenters) and len(oldCenters) == CLUSTERS_COUNT

		for i in range(0, CLUSTERS_COUNT):
			distanceBetweenOldAndNew = np.linalg.norm(np.array(oldCenters[i]) - np.array(newCenters[i]))
			differenceAboveIgnorableDefined = distanceBetweenOldAndNew > IGNORABLE_CLUSTER_MOVE_DISTANCE
			shouldContiune = shouldContiune or differenceAboveIgnorableDefined

		return shouldContiune


	@staticmethod
	def getNearestClusterCoords(coordinates, clusterCoordinates):
		minDistance = None
		nearestClusterCoords = None


		for clusterCoord in clusterCoordinates:
			distanceToCluster = np.linalg.norm(np.array(coordinates) - np.array(clusterCoord))
			
			if minDistance is None or minDistance > distanceToCluster:
				minDistance = distanceToCluster
				nearestClusterCoords = clusterCoord

		return nearestClusterCoords


	@staticmethod
	def calculateNewClusterCenters(clusterForHt, clusterCenters, htVectors):
		newClusterCenters = [[0] * len(clusterCenters[0])]*len(clusterCenters)
		countOfHtForNewClusterCenterByIdx = [0]*len(clusterCenters)


		# after this for loop, the new clusters are the sum of all vectors in the previous ones
		for ht in clusterForHt:
			indexOfCenterToUpdate = clusterCenters.index(clusterForHt[ht])
			newClusterCenters[indexOfCenterToUpdate] = np.add(newClusterCenters[indexOfCenterToUpdate], htVectors[ht])
			countOfHtForNewClusterCenterByIdx[indexOfCenterToUpdate] += 1 

		# now divide them by the count of vectors in them to get the average

		for i in range(0, len(newClusterCenters)):
			newClusterCenters[i] = np.rint(np.divide(newClusterCenters[i], countOfHtForNewClusterCenterByIdx[i])).astype(int).tolist()

		return newClusterCenters

