from flask import Flask

app = Flask(__name__)
port = 5234
host = '127.0.0.1'

@app.route('/')
def index():
    return 'Hello world'

@app.route('/kurvi')
def whatever():
	return 'Belo!'

@app.before_first_request
def seed():
	print("Seeding db...")

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
