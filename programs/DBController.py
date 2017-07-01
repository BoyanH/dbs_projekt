import psycopg2
import json
from Contract import Contract
from Utils import Utils


class DBController:

	dbUser = "testuser"
	dbName = "Election"
	host = "localhost"
	dbUserPassword = "testpass"

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
			if table != Contract.TABLE_WEEK:
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
		# 	self.addToDB(table, data)
		# except Exception as err:
		# 	print("Something went wrong: " + str(err))


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

	@staticmethod
	def getWhereConditionsForUpdate(columnsDict):
		
		conditions = []

		for key in columnsDict:
			conditions.append(key + '=' + "'{0}'".format(columnsDict[key]))

		return ' AND '.join(conditions)

