from flask import render_template, jsonify, make_response
from app import app
from flask import request
import monkey
import json
import numpy as np
import os
from collections import Counter
import tweepy
import re
import csv
from random import shuffle

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
def graph3(chartID = 'chart_ID',chart_type = 'pie', chart_height = 500):
	twitter_user = request.args.get('ID')
	twitter_self = request.args.get('ID_self')
	max_topics = 6

	#read user's tweets
	topics_user=[]
	rel_user=[]
	tweets_read=Counter()
	filename = os.path.join('app','static','%s_tweets_histogram.csv' % twitter_user)
	print filename
	with open(filename, 'r') as f:
		for line in f:
			tweets_read[line.split(',')[0]] = int(line.split(',')[1])
	
	        
	with open(os.path.join('app','static','%s_tweets_categorized.csv' % twitter_user),'r') as data_file:    
		tweets_categorized = json.load(data_file)
		
	data=[]
	for topic, count in tweets_read.most_common(max_topics):	
		topic.strip()
		s = {}
		#s['name'] = topic
		s['y'] = count
	#	s['drilldown'] =  "cars"

		#get example of texts
		tweet_scored = tweets_categorized[topic.strip()]
		relevance = Counter()
		for l,m in tweet_scored:
			relevance[ l[0]] = m
		k = relevance.most_common(1)
		s['name'] = topic
		text = k[0][0].encode('utf-8')
		s['Tweetex'] = text
		data.append(s)
		
		text = k[0][0]
		
		print topic,text


	

	#print tweets_categorized	
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'your friend', "data": data}]
   
	title = {"text": 'Your friend\'s interests'}
	xAxis = {"categories":topics_user}
	#print xAxis
	yAxis = {"title": {"text": 'relevance'}}
	
	
	
	return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'yAxis Label'}}
	return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
   
@app.route('/output_old')
#global prof=[]
#def call_output(): 
#	twitter_user = request.args.get('ID')
#	prof = monkey.twitterProfile(twitter_user)
#	return render_template("output.html", the_result = prof)

def graph2(chartID = 'chart_ID', chartID2 = 'chart_ID2',chart_type = 'bar', chart_height = 500):
	twitter_user = request.args.get('ID')
	twitter_self = request.args.get('ID_self')
	max_tpoics = 5
	
	print "I am here"
	print twitter_user
	print twitter_self
	
	#get user's topics
	prof = monkey.twitterProfile(twitter_user)
	
	#get self topics
	prof_self = monkey.twitterProfile(twitter_self)
	print (prof)
	print (prof_self)
	topics_user=[]
	rel_user=[]
	rel_user_self=[]
   	for l,m in prof[:max_tpoics]:
   		thistopic = l.encode('utf-8')
   		print(thistopic)
		topics_user.append(thistopic)
		rel_user.append(m)
		
		#search in the self profile on relevance to topics of user
		[i for i, v in enumerate(prof_self) if v[0].encode('utf-8') == thistopic]
		print i
		print v[0].encode('utf-8')
		print v[1]
		
		[item for item in prof_self if thistopic in item]
		if item is not None:
	#		print item[0]
			rel_user_self.append(item[1])
		else:
			rel_user_self.append(0)
		
	
	topics_self=[]
	rel_self=[]
	rel_self_user=[]
	count=0
   	for l,m in prof_self[:max_tpoics]:
   		thistopic = l.encode('utf-8')
		topics_self.append(thistopic)
		rel_self.append(m)
		
		#search in the user profile on relevance to topics of self
		[item for item in prof if thistopic in item]
		if item is not None:
			#print item[1]
			rel_self_user.append(item[1])
		else:
			rel_self_user.append(0)	
		
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'your friend', "data": rel_user}, {"name": 'yourself', "data": rel_self}]
	title = {"text": 'Your friend\'s interests'}
	#xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	#print xAxis
	xAxis = {"categories":topics_user}
	#print xAxis
	yAxis = {"title": {"text": 'relevance'}}
	
	chart2 = {"renderTo": chartID2, "type": chart_type, "height": chart_height,}
	series2 = [{"name": 'yourself', "data": rel_self}, {"name": 'your friend', "data": rel_self_user}]
	title2 = {"text": 'My Title'}
	#xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	#print xAxis
	xAxis2 = {"categories":topics_self}
	#print xAxis
	yAxis2 = {"title": {"text": 'relevance'}}
	
	return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, 
	chartID2=chartID2, chart2=chart2, series2=series2, title2=title2, xAxis2=xAxis2, yAxis2=yAxis2)
	#return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
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
