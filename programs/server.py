from flask import Flask
from cleaner import cleanData
from DBController import DBController
from TableParser import TableParser

app = Flask(__name__)
port = 5234
host = '127.0.0.1'

@app.route('/')
def index():
	return 'Hello world'

if __name__ == '__main__':

	dbController = DBController()
	filled = dbController.checkFilled()

	if not filled:
		cleanData()
		TableParser.parseTables()
	else:
		print('Data already imported :)')

	app.run(debug=True, host=host, port=port)
