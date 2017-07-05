from DBController import DBController
from Contract import Contract 

from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from io import BytesIO

# value to return if hashtag is not found
HASHTAG_NOT_FOUND = '404hashtag'

def dailyTotalHashtags():
	dbc = DBController()

	usage = dbc.getTotalHashtagUsage(Contract.TABLE_DAY)

	#return str(usage)
	return plotUsage(usage)



def plotUsage(data):
	fig = Figure()
	ax = fig.add_subplot(111)

	# x is date, y is count
	# can't plot strings tho
	labels_x = [x[0] for x in data]
	x = np.arange(len(labels_x))
	y = [x[1] for x in data]
	
	ax.bar(x,y, align='center', color='y')
	
	# set labels every N colums
	N = 4
	ax.set_xticks(np.arange(len(x), step=N))
	ax.set_xticklabels([labels_x[i] for i in np.arange(len(x), step=N)])

	# use the plotted data as a HTTP response
	canvas = FigureCanvas(fig)
	png_output = BytesIO()
	canvas.print_png(png_output)

	response=make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	
	return response
