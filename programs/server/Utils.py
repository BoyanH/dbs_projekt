import uuid

class Utils:

	@staticmethod
	def getUniquePairs(arr):

		if len(arr) < 2:
			return []

		pairs = []

		for i, itemA in enumerate(arr):

			for j, itemB in enumerate(arr[(i+1):]):

				crntPair = [itemA, itemB]
				crntPair.sort()
				pairs.append(crntPair)

		return pairs

	@staticmethod
	def getRandom8ByteInt():
		return uuid.uuid4().int & (1 << (8*8 - 1))-1

	@staticmethod
	def getValuesFromDict(entriesDict):
		sqlValuesArr = []
		for key in entriesDict:
			escapedString = str(entriesDict[key]).replace('`', '\\`').replace('\'', '\\`')
			sqlValuesArr.append('\'{0}\''.format( escapedString ))
		return ', '.join(sqlValuesArr)
	