import psycopg2
import json
from Contract import Contract


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
		
		sqlExpr = "INSERT INTO {0} ({1}) VALUES ({2})"
		sqlCommand = sqlExpr.format(table, ",".join(list(entriesDict.keys())), DBController.getValuesFromDict(entriesDict))

		try:
			self.cursor.execute(sqlCommand)
		except Exception as err:
			print("Something went wrong while adding new DB entry: " + str(err))

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

	@staticmethod
	def getValuesFromDict(entriesDict):
		sqlValuesArr = []
		for key in entriesDict:
			escapedString = str(entriesDict[key]).replace('`', '\\`')
			sqlValuesArr.append('\'{0}\''.format( escapedString ))
		return ', '.join(sqlValuesArr)
