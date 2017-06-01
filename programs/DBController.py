import psycopg2

class DBController:

    dbUser = "testuser"
    dbName = "dbs"
    host = "localhost"
    dbUserPassword = "testpass"

    connectionStringTemplate = "dbname='{0}' user='{1}' host='{2}' password='{3}'"
    connectionString = connectionStringTemplate.format(dbName, dbUser, host, dbUserPassword)

    def __init__(self):
        print("Connected to DB!")
        self.connection = psycopg2.connect(connectionString)    
        self.c = connection.cursor()

	def addToDB(self, table, entriesDict):
		
		sqlExpr = "INSERT INTO {0} ({1}) VALUES ({2})"
		sqlCommand = sqlExpr.format(table, list(entriesDict.keys), self.getValuesFromDict(entriesDict))

        try:
		    c.execute(sqlCommand)
		    connection.commit()
        except Exception as er:
            print("Something went wrong while adding new DB entry: " + er)

    def getValuesFromDict(entriesDict):
        sqlValuesArr = []
        for key in entriesDict:
            sqlValuesArr.append('\'{0}\''.format(entriesDict[key]))
        return ', '.join(str(e) for e in sqlValuesArr)

    def close(self):
        self.connection.close
