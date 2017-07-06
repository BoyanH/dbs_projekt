from DBController import DBController
from Contract import Contract 

from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from io import BytesIO

# value to return if hashtag is not found
HASHTAG_NOT_FOUND = '404hashtag'

# Total hashtag usage, with date increment = DAY
def dailyTotalHashtags():
	dbc = DBController()
	usage = dbc.getTotalHashtagUsage(Contract.TABLE_DAY)
	dbc.close()

	#return str(usage)
	return plotUsage(usage)

# Total hashtag usage with date increment = WEEK
def weeklyTotalHashtags():
	dbc = DBController()
	usage = dbc.getTotalHashtagUsage(Contract.TABLE_WEEK)
	dbc.close()

	return plotUsage(usage)

# Specific hashtag usage with weekly increments
def weeklyHashtag(hashtag):
	if not hashtag:
		return '404';
	
	dbc = DBController()
	
	# get weeks and get weeks and count of hashtag usage
	# need to merge the two lists, because 'usage' does
	# not contain every week date (becase usage is 0)
	weeks = dbc.getDates(Contract.TABLE_WEEK)
	usage = {key: value for (key, value) in dbc.getUsageForHashtag(hashtag, Contract.TABLE_WEEK)}

	data_to_plot = [[x, usage[x]] if x in usage else [x, 0] for x in weeks ]
	
	dbc.close()

	return plotUsage(data_to_plot, hashtag, increment='Weekly')

# Specific hashtag usage with daily increments
def dailyHashtag(hashtag):
	if not hashtag:
		return '404';
	
	dbc = DBController()
	
	# get days and get days and count of hashtag usage
	# need to merge the two lists, because 'usage' does
	# not contain every day date (becase usage is 0)
	days = dbc.getDates(Contract.TABLE_DAY)
	usage = {key: value for (key, value) in dbc.getUsageForHashtag(hashtag, Contract.TABLE_DAY)}

	data_to_plot = [[x, usage[x]] if x in usage else [x, 0] for x in days ]
	
	dbc.close()

	return plotUsage(data_to_plot, hashtag, increment='Daily')

def plotUsage(data, hashtag=None, increment=''):
	fig = Figure(figsize=(15,10), dpi=80)
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
	ax.set_xticklabels([labels_x[i] for i in np.arange(len(x), step=N)], rotation='vertical')

	# names
	if(hashtag):
		fig.suptitle(increment + ' plot of usage of ' + hashtag, fontsize=20)
	else:
		fig.suptitle('Total hashtag usage: ', fontsize=20)
	
	# use the plotted data as a HTTP response
	canvas = FigureCanvas(fig)
	png_output = BytesIO()
	canvas.print_png(png_output)

	response=make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	
	return response
