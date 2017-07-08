import psycopg2
import json
from Contract import Contract
from Utils import Utils
import os

class DBController:

	dbUser = os.environ.get('DB_USER_HEROKU', "testuser")
	dbName = os.environ.get('DB_NAME_HEROKU', "Election")
	host = os.environ.get('DB_HOST_HEROKU', "localhost")
	dbUserPassword = os.environ.get('DB_PASSWORD_HEROKU', "testpass")

	connectionStringTemplate = "dbname='{0}' user='{1}' host='{2}' password='{3}'"
	connectionString = connectionStringTemplate.format(dbName, dbUser, host, dbUserPassword)

	def __init__(self):
		print("Connected to DB!")
		self.connection = psycopg2.connect(DBController.connectionString)	 
		self.cursor = self.connection.cursor()

	def addToDB(self, table, entriesDict):
		
		sqlInsertExpr = "INSERT INTO {0} ({1}) VALUES ({2})"
		sqlInsertCommand = sqlInsertExpr.format(table, ",".join(list(entriesDict.keys())), Utils.getValuesFromDict(entriesDict))

		try:
			if Contract.COUNT_COLUMN in entriesDict:

				entriesDictCopy = entriesDict.copy()
				del entriesDictCopy[Contract.COUNT_COLUMN]

				sqlSelectExpr = "SELECT {1} FROM {0} WHERE {2}"
				sqlSelectCommand = sqlSelectExpr.format(table, ",".join(list(entriesDict.keys())), DBController.getWhereConditionsForUpdate(entriesDictCopy))

				sqlUpdateExpr = "UPDATE {0} SET {1}={1}+1 WHERE ({2})"
				sqlUpdateCommand = sqlUpdateExpr.format(table, Contract.COUNT_COLUMN, DBController.getWhereConditionsForUpdate(entriesDictCopy))

				self.cursor.execute(sqlSelectCommand)
				results = self.cursor.fetchall()

				if len(results) > 0:
					self.cursor.execute(sqlUpdateCommand)
				else:
					self.cursor.execute(sqlInsertCommand)
			else:
				self.cursor.execute(sqlInsertCommand)
		except Exception as err:
			if table != Contract.TABLE_WEEK and table != Contract.TABLE_DAY:
				print("Something went wrong while adding new DB entry to table {0}: {1}".format(table, err))

		self.connection.commit()

	def close(self):
		self.connection.close
		print("DB connection closed!")

	def handleAddTable(self, data):
		table = data[Contract.ADD_TO_TABLE_KEY]
		del data[Contract.ADD_TO_TABLE_KEY]
		self.addToDB(table, data)
		# try:
		#	self.addToDB(table, data)
		# except Exception as err:
		#	print("Something went wrong: " + str(err))


	def addMultiple(self, *tableLists):
		
		for tableList in tableLists:

			if isinstance(tableList, list):

				for table in tableList:
					self.handleAddTable(table)
			else:
				self.handleAddTable(tableList)

	def checkFilled(self):

		self.cursor.execute("SELECT * FROM {0}".format(Contract.TABLE_WEEK))
		weeks = self.cursor.fetchall()

		return len(weeks) > 0

	def getTopTweets(self):
		self.cursor.execute("SELECT * FROM {0} ORDER BY {1} LIMIT 10".format(Contract.TABLE_TWEET, Contract.RATING_COLUMN))
		return self.cursor.fetchall()

	def getHashtagTexts(self):
		self.cursor.execute("SELECT {0} FROM {1} ORDER BY {0}".format(Contract.TEXT_LOWER_CASE_COLUMN, Contract.TABLE_HASHTAG))
		return [x[0] for x in self.cursor.fetchall()]

	def getDates(self, dateTable):
		dateColumn = Contract.START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DATE_COLUMN

		self.cursor.execute("SELECT {0} FROM {1} ORDER BY {0}".format(dateColumn, dateTable))
		return [x[0] for x in self.cursor.fetchall()]

	def getDatesForHashtag(self, hashTagText, dateTable):
		dateColumn = Contract.START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DATE_COLUMN
		middleTable = Contract.TABLE_USED_IN if dateTable == Contract.TABLE_WEEK else Contract.TABLE_USED_ON
		joinOnDateColumn =	Contract.WEEK_START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DAY_DATE_COLUMN

		# Example:
		# SELECT startdate FROM hashtag, week, usedin 
		# WHERE hashtagtext = textlowercase AND date = startdate 
		# AND hashtagtext = 'votetrump2016'

		self.cursor.execute("SELECT {0} FROM {1} WHERE {2}".format(
			dateColumn, 
			', '.join([Contract.TABLE_HASHTAG, dateTable, middleTable]),
			'{0} = {1} AND {2} = {3} AND {4} = {5}'.format(
				Contract.HASHTAG_TEXT_COLUMN, Contract.TEXT_LOWER_CASE_COLUMN,
				joinOnDateColumn, dateColumn,
				Contract.TEXT_LOWER_CASE_COLUMN, "'{0}'".format(hashTagText)
				)
			)
		)

		return [x[0] for x in self.cursor.fetchall()]

	def getUsageForHashtag(self, hashtagText, dateTable):
		dateColumn = Contract.WEEK_START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DAY_DATE_COLUMN
		middleTable = Contract.TABLE_USED_IN if dateTable == Contract.TABLE_WEEK else Contract.TABLE_USED_ON
		dateColumn2 = Contract.START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DATE_COLUMN
		
		# Example:
		# SELECT startdate, SUM(count) FROM week, usedin WHERE startdate = weekstartdate
		# AND hashtagtext='votetrump2016' GROUP BY startdate;

		self.cursor.execute("SELECT {0}, SUM({1}) FROM {2}, {3}  WHERE {0} = {4} AND {5} = '{6}' GROUP BY {0}".format(
									dateColumn, Contract.COUNT_COLUMN,		#SELECT
									dateTable,middleTable,					#FROM
									dateColumn2, Contract.HASHTAG_TEXT_COLUMN, hashtagText))	#WHERE .. GROUP BY 

		return [x for x in self.cursor.fetchall()]

	def getTotalHashtagUsage(self, dateTable):
		dateColumn = Contract.WEEK_START_DATE_COLUMN if dateTable == Contract.TABLE_WEEK else Contract.DAY_DATE_COLUMN
		middleTable = Contract.TABLE_USED_IN if dateTable == Contract.TABLE_WEEK else Contract.TABLE_USED_ON
	
		# Example:
		# SELECT weekstartdate, SUM(count) FROM usedin GROUP BY weekstartdate

		self.cursor.execute("SELECT {0}, SUM({1}) FROM {2} GROUP BY {3}".format(
									dateColumn, Contract.COUNT_COLUMN, middleTable, dateColumn))

		return [x for x in self.cursor.fetchall()]

	def getClusterCoordinates(self):
	
		# SELECT textlowercase, belogstoclusterid. coordinates2d
		# FROM hasgtag

		self.cursor.execute("SELECT {0}, {1}, {2} FROM {3}".format(
			Contract.TEXT_LOWER_CASE_COLUMN, Contract.BELONGS_TO_CLUSTER_ID, 
			Contract.COORDINATES_2D_COLUMN, Contract.TABLE_HASHTAG))

		return self.cursor.fetchall()

		# Example:
		# SELECT textlowercase, hashtag.belongstoclusterid, coordinates2d, edgewidth 
		# FROM representationedge, hashtag 
		# WHERE representationedge.belongstoclusterid = hashtag.belongstoclusterid 
		# AND (textlowercase = hashtag1 OR textlowercase = hashtag2);

		#self.cursor.execute("SELECT {0}, {1}.{2}, {3}, {4} FROM {5}, {1} WHERE {5}.{2} = {1}.{2} AND ({0} = {6} OR {0} = {7})".format(
		#	Contract.TEXT_LOWER_CASE_COLUMN, Contract.TABLE_HASHTAG, Contract.BELONGS_TO_CLUSTER_ID, #SELECT
		#	Contract.COORDINATES_2D_COLUMN, Contract.EDGE_WIDTH_COLUMN, 
		#	Contract.TABLE_REPRESENTATION_EDGE,						#FROM
		#	Contract.HASHTAG1_COLUMN, Contract.HASHTAG2_COLUMN))	#WHERE

		#return self.cursor.fetchall()

	def getEdgeSizes(self):

		# Example:
		# SELECT hashtag1, hashtag2, edgewidth
		# FROM representationedge

		self.cursor.execute("SELECT {0}, {1}, {2} FROM {3}".format(
				Contract.HASHTAG1_COLUMN, Contract.HASHTAG2_COLUMN, Contract.EDGE_WIDTH_COLUMN, Contract.TABLE_REPRESENTATION_EDGE))

		return self.cursor.fetchall()



	def getUsedTogetherWithPairsForHashtag(self, hashTagText):
		self.cursor.execute("SELECT {0} FROM {1} WHERE {2}".format(
			', '.join([Contract.PRIMARY_HASHTAG_COLUMN, Contract.TOGETHER_WITH_HASHTAG_COLUMN, Contract.COUNT_COLUMN]), 
			Contract.TABLE_USED_TOGETHER_WITH,
			'{0} = {1} OR {2} = {3}'.format(
				Contract.PRIMARY_HASHTAG_COLUMN, "'{0}'".format(hashTagText),
				Contract.TOGETHER_WITH_HASHTAG_COLUMN, "'{0}'".format(hashTagText),
				)
			)
		)

		return self.cursor.fetchall()

	def updateHashtagVector(self, hashTagText, vector, column):
		sqlUpdateExpr = "UPDATE {0} SET {1}={2} WHERE {3}"
		sqlUpdateCommand = sqlUpdateExpr.format(
			Contract.TABLE_HASHTAG, 
			column, '\'{' + ', '.join([str(x) for x in vector]) + '}\'',
			'{0} = \'{1}\''.format(Contract.TEXT_LOWER_CASE_COLUMN, hashTagText)
		)

		self.cursor.execute(sqlUpdateCommand)

	def getCoordinatesOfHashtag(self, hashTagText):
		self.cursor.execute("SELECT {0} FROM {1} WHERE {2} = '{3}'".format(
			Contract.COORDINATES_COLUMN, Contract.TABLE_HASHTAG, Contract.TEXT_LOWER_CASE_COLUMN, hashTagText
			)
		)

		return [x[0] for x in self.cursor.fetchall()]

	def addClusterCenter(self, center):
		sqlInsertExpr = "INSERT INTO {0} ({1}) VALUES ({2})"
		sqlInsertCommand = sqlInsertExpr.format(Contract.TABLE_CLUSTER, Contract.CENTER_COORDINATES, DBController.getSQLArrayFromList(center))

		self.cursor.execute(sqlInsertCommand)

	def addHashtagToCluster(self, hashtag, clusterId):
		sqlUpdateExpr = "UPDATE {0} SET {1}={2} WHERE {3} = {4}"
		sqlUpdateCommand = sqlUpdateExpr.format(Contract.TABLE_HASHTAG, Contract.BELONGS_TO_CLUSTER_ID, "'{0}'".format(clusterId),
			Contract.TEXT_LOWER_CASE_COLUMN, "'{0}'".format(hashtag))

		self.cursor.execute(sqlUpdateCommand)

	def getClusterCenterId(self, coords):
		self.cursor.execute("SELECT {0} FROM {1} WHERE {2} = {3}".format(Contract.ID_COLUMN, Contract.TABLE_CLUSTER,
			Contract.CENTER_COORDINATES, '\'{' + ', '.join([str(x) for x in coords]) + '}\''))

		return [x[0] for x in self.cursor.fetchall()][0]

	def addRepresentationEdge(self, htA, htB, clusterId, edgeWidth):
		sqlInsertExpr = "INSERT INTO {0} ({1}) VALUES ({2})"
		sqlInsertCommand = sqlInsertExpr.format(
			Contract.TABLE_REPRESENTATION_EDGE, # INSERT INTO
			','.join([Contract.HASHTAG1_COLUMN, Contract.HASHTAG2_COLUMN, Contract.BELONGS_TO_CLUSTER_ID, Contract.EDGE_WIDTH_COLUMN]), # VALUES (...)
			', '.join(["'{}'".format(str(x)) for x in [htA, htB, clusterId, edgeWidth] ]) # (...)
		)

		self.cursor.execute(sqlInsertCommand)

	def getAuthors(self):
		sqlSelect = "SELECT {0}, count(*) FROM {1} GROUP BY {2} ORDER BY count(*)"
		sqlCommand = sqlSelect.format(
			Contract.AUTHOR_COLUMN,
			Contract.TABLE_TWEET,
			Contract.AUTHOR_COLUMN
		)

		self.cursor.execute(sqlCommand)
		return [ [x[0], x[1]] for x in self.cursor.fetchall()]

	def getTweets(self, author=None):
		sqlSelect = "SELECT {0} FROM {1}" +  (" WHERE {2} = '{3}' and {4} = {5} " if author != None else "") + "GROUP BY {6} ORDER BY {7} DESC"
		sqlCommand = sqlSelect.format(
			', '.join([Contract.AUTHOR_COLUMN, Contract.TEXT_COLUMN, Contract.TIME_COLUMN, Contract.ID_COLUMN, Contract.HASHTAG_TEXT_COLUMN]), # SELECT
			','.join([Contract.TABLE_TWEET, Contract.TABLE_CONTAINS]),
			Contract.AUTHOR_COLUMN, author, Contract.TWEET_ID_COLUMN, Contract.ID_COLUMN,
			','.join([Contract.AUTHOR_COLUMN, Contract.TEXT_COLUMN, Contract.TIME_COLUMN, Contract.ID_COLUMN, Contract.HASHTAG_TEXT_COLUMN]), 
			'count(*)'
		)

		self.cursor.execute(sqlCommand)
		return [ [str(z) for z in x][:4] for x in self.cursor.fetchall()]

	def getHashtagsByTweet(self, tweetId):
		sqlSelect = "SELECT {0} FROM {1} WHERE {2} ORDER BY {3}"
		sqlCommand = sqlSelect.format(
			','.join([Contract.TEXT_LOWER_CASE_COLUMN, Contract.COUNT_COLUMN]),					# SELECT
			','.join([Contract.TABLE_HASHTAG, Contract.TABLE_TWEET, Contract.TABLE_CONTAINS]),	# FROM
			"{0} = {1} AND {2} = {3} AND {4} = '{5}'".format(									# WHERE
					Contract.HASHTAG_TEXT_COLUMN, Contract.TEXT_LOWER_CASE_COLUMN,
					Contract.TWEET_ID_COLUMN, Contract.ID_COLUMN,
					Contract.TWEET_ID_COLUMN, tweetId
				),
			Contract.COUNT_COLUMN 																# ORDER BY
		)

		self.cursor.execute(sqlCommand)
		print(sqlCommand)
		return [ [z for z in x] for x in self.cursor.fetchall()]

	@staticmethod
	def getWhereConditionsForUpdate(columnsDict):
		
		conditions = []

		for key in columnsDict:
			conditions.append(key + '=' + "'{0}'".format(columnsDict[key]))

		return ' AND '.join(conditions)

	@staticmethod
	def getSQLArrayFromList(arr):
		return '\'{' + ', '.join([str(x) for x in arr]) + '}\''
