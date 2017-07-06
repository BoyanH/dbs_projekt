class ClusteringRepresentation:

	@staticmethod
	def getEdgeWidthFromDistance(distance):
		if distance < 50:
			return 5
		elif distance < 100:
			return 4
		elif distance < 150:
			return 3
		elif distance < 250:
			return 2
		else:
			return 1
