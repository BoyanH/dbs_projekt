from DBController import DBController
from Contract import Contract
import numpy as np
from random import randint
from sklearn.manifold import TSNE

CLUSTERS_COUNT = 7
IGNORABLE_CLUSTER_MOVE_DISTANCE = 1
USED_TOGETHER_WITH_WEIGHT = 1
DATE_WEIGHT = 3
DATE_TABLE = Contract.TABLE_WEEK

REDUCED_DIMENSIONS_AMOUNT = 10
TSNE_PERPLEXITY = 30.0

class Cluster:

	def __init__(self):
		self.dBController = DBController();
		self.hashtagTexts = self.dBController.getHashtagTexts()
		self.dates = self.dBController.getDates(DATE_TABLE)

		hashtagDimensionMapper = {}
		dayDimensionMapper = {}
		counter = 0

		for text in self.hashtagTexts:
			hashtagDimensionMapper[text] = counter
			counter += 1

		for date in self.dates:
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

		print('Executing k-means algorithm...')

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

			dates = self.dBController.getDatesForHashtag(ht, DATE_TABLE)
			pairs = self.dBController.getUsedTogetherWithPairsForHashtag(ht)

			for date in dates:
				dimensionForDate = self.dayDimensionMapper[date]
				htVectors[ht][dimensionForDate] += DATE_WEIGHT

			# add count of usedTogetherWith to the 2 dimensions of a vector corresponding to the 2 hashtag texts
			for pair in pairs:

				for i in range(2):
					dimensionForHt = self.hashtagDimensionMapper[pair[i]]
					htVectors[ht][dimensionForHt] += pair[2]*USED_TOGETHER_WITH_WEIGHT #pair[2] = count

		reducedVectors = Cluster.reduceVectorDimensions(htVectors)

		return reducedVectors;

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

	@staticmethod
	def reduceVectorDimensions(vectorsDictionary):
		# X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])


		(vectorSpace, keyToIdx) = Cluster.getVectorSpaceForVectors(vectorsDictionary)

		model = TSNE(n_components = REDUCED_DIMENSIONS_AMOUNT, random_state=0)
		np.set_printoptions(suppress=True)

		print("Reducing {0} dimensional vector space into {1} dimensional...".format( str(len(vectorSpace[0])), str(REDUCED_DIMENSIONS_AMOUNT) ))
		reducedVectorSpace = model.fit_transform(vectorSpace)
		reducedVectorsDictionary = Cluster.orderVectorSpaceIntoDict(reducedVectorSpace, keyToIdx)

		return reducedVectorsDictionary

	@staticmethod
	def getVectorSpaceForVectors(vectorsDictionary):
		vectorSpace = []
		idx = 0
		keyToIdx = {}

		for vKey in vectorsDictionary:
			vectorSpace.append(vectorsDictionary[vKey])
			keyToIdx[vKey] = idx
			idx += 1

		return (np.array(vectorSpace), keyToIdx)

	@staticmethod
	def orderVectorSpaceIntoDict(vectorSpace, keyToIdxDict):
		vectorSpaceDict = {}

		for key in keyToIdxDict:
			index = keyToIdxDict[key]
			vectorSpaceDict[key] = vectorSpace[index].tolist()

		return vectorSpaceDict

