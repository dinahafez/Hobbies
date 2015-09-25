from __future__ import division
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


user_topics={}

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
def graph(chartID = 'chart_ID',chart_type = 'pie', chart_height = 500):
	twitter_user = request.args.get('ID')
	max_topics = 6
	
	#read user's tweets
	topics_user=[]
	rel_user=[]
	tweets_read=Counter()
	try:
		filename = os.path.join('app','static','%s_tweets_histogram.csv' % twitter_user)
		with open(filename, 'r') as f:
			for line in f:
				tweets_read[line.split(',')[0]] = int(line.split(',')[1])
				
		with open(os.path.join('app','static','%s_tweets_categorized.csv' % twitter_user),'r') as data_file:    
			tweets_categorized = json.load(data_file)
		
		data=[]
		total=0
		for topic, count in tweets_read.most_common(max_topics):	
			total = total + int(count)
			
		for topic, count in tweets_read.most_common(max_topics):	
			topic.strip()
			s = {}
			s['y'] = count
			user_topics[topic.strip()] =  (count/total*100)
			print count
			print total
			print (count/total)
			print  (count/total*100)
			#get example of tweets
			tweet_scored = tweets_categorized[topic.strip()]
			relevance = Counter()
			for l,m in tweet_scored:
				relevance[ l[0]] = m
			k = relevance.most_common(4)
			s['name'] = topic		
			s['Tweetex1'] = k[0][0].encode('utf-8')
			s['Tweetex2'] = k[1][0].encode('utf-8')
			s['Tweetex3'] = k[2][0].encode('utf-8')
			#s['Tweetex4'] = k[3][0].encode('utf-8')
		
			data.append(s)
	
		#print user_topics
		#print tweets_categorized	
		chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
		series = [{"name": 'Your friend', "data": data}]
   
		title = {"text": ''}
		xAxis = {"categories":topics_user}
		yAxis = {"title": {"text": 'relevance'}}
	
		return render_template('high.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
	except:
		return render_template('error.html')

@app.route('/common')
def common(chartID = 'chart_ID',chart_type = 'bar', chart_height = 500):
	twitter_user = request.args.get('ID_self')
	max_topics = 6
	print "in the function"
	print user_topics
	
	common = []
	tweets_read=Counter()
	try:
		filename = os.path.join('app','static','%s_tweets_histogram.csv' % twitter_user)
		print filename
		with open(filename, 'r') as f:
			for line in f:
				tweets_read[line.split(',')[0]] = int(line.split(',')[1])
				
	#	with open(os.path.join('app','static','%s_tweets_categorized.csv' % twitter_user),'r') as data_file:    
	#		tweets_categorized = json.load(data_file)
		
		data=[]
		friend=[]
		me=[]
		total=0
		for topic, count in tweets_read.most_common(max_topics):	
			total = total + int(count)
	
		for topic, count in tweets_read.most_common(max_topics):
			if topic.strip() in user_topics:
				print "trying to find " + topic
				print user_topics[topic.strip()]
				common.append(topic.strip())
				friend.append(int(user_topics[topic.strip()]))
				me.append((count/total * 100))
			else:
				print topic + "does not exits"
#				print topic +	 "does not exist"
			
		print common
		
		print friend
		print me
		#print user_topics
		#print tweets_categorized	
		chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
		series = [{"name": 'Friend\'s interests', "data": friend}, {"name": 'Your interests', "data": me}]
		title = {"text": ''}
		xAxis = {"categories": common, "labels":{"style":{"fontSize": '17px'}}}
		
		yAxis = {"title": {"text": 'score'}, "labels":{"style":{"fontSize": '17px'}}}
		
		return render_template('common.html', interest1 = common[0], interest2=common[1], interest3=common[2], interest4=common[3], interest5=common[4], interest6=common[5], chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
	except:
		return render_template('error.html')
		
		
@app.route('/d3')
def d3_try():	
	return render_template("d3.html")
	
	