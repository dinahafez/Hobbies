from flask import render_template, jsonify, make_response
from app import app
from flask import request
import monkey
import json
import numpy as np


@app.route('/')
def index():
   user = '' # fake user
   return render_template("index.html",
       title = 'Home',
       user = user)

@app.route('/input')
def input():
  return render_template("input.html")
  
@app.route('/output')
#global prof=[]
#def call_output(): 
#	twitter_user = request.args.get('ID')
#	prof = monkey.twitterProfile(twitter_user)
#	return render_template("output.html", the_result = prof)

def graph2(chartID = 'chart_ID', chart_type = 'bar', chart_height = 500):
	twitter_user = request.args.get('ID')
	prof = monkey.twitterProfile(twitter_user)
	
	x=[]
	y=[]
   	for l,m in prof[:3]:
		x.append(l.encode('utf-8'))
		y.append(m)
	
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": y}, {"name": 'Label2', "data": y}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	print xAxis
	xAxis = {"categories":x}
	#print xAxis
	yAxis = {"title": {"text": 'relevance'}}
	
	return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
	#return render_template("output.html", the_result = x)
   
@app.route('/d3')
def d3_try():	
	return render_template("d3.html")
	
@app.route('/bulletdata')
def data():
	filename = 'app/static/bulletdata.json'
	bulletdata = {'children':[]}
	with open(filename, 'r') as infile:
		bulletdata['children'] = json.load(infile)
	return jsonify(bulletdata)
	
	
	
#@app.route("/priceplot.png")
#def priceplot():
#	x=np.array([1,2,3,4,5,6])
#	y=np.array([1,2,3,4,5,6])
#	response = monkey.graph_prices(x,y,'stuff')
#	return response
	
@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'bar', chart_height = 500):
	x=[]
	y=[]
   	for l,m in prof:
		x.append(l)
		y.append(m)
		
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'relevance'}}
	return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)