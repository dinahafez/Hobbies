import requests
import json
import pandas as pd
from pandas import DataFrame
import json
import operator
import os
import sys
import numpy as np
import StringIO
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

	
#NASA spacex

def twitterProfile (user): 
 	
 	data = {
	"twitter_user_name": user,
	"twitter_access_token_key": os.environ['access_key'],
	"twitter_consumer_key": os.environ['consumer_key'],
	"twitter_consumer_secret": os.environ['consumer_secret'],
	"twitter_access_token_secret": os.environ['access_secret']
	}
		
	
	response = requests.post(
        "https://api.monkeylearn.com/v2/pipelines/pi_JJ9JrKvk/run/", 
        data=json.dumps(data),
        headers={'Authorization': 'Token 2984a680eb9c9032b6e5dde29902190f181022fb',
        'Content-Type': 'application/json'})
	a = response.json()

	profile = a['result']['user_profiling']

	keywords = a['result']['keywords']
	keyDict = keywords[0]['keywords']

    #for i, entry in enumerate(keyDict):
    #    print entry['keyword'],entry['relevance']


    #print ("*********uers profile*********")
	sorted_profile = sorted(profile.items(), key= operator.itemgetter(1),reverse=True)
	dict(sorted_profile) == profile


	#for i, entry in enumerate(sorted_profile):
		#print entry

    #type (sorted_profile)
	return sorted_profile;
	
def graph_prices (x,y,gname):
	fig = Figure(facecolor='white')
	ax=fig.add_subplot(111)
	ax.plot_date(x, y, '-')
	ax.set_ylim([0,np.max(y) + np.max(y) * 10])
	ax.set_xlabel('Time')
    
	#formatter = FuncFormatter(money_format)
    
	#ax.yaxis.set_major_formatter(formatter)
	#fig.autofmt_xdate()
    
	canvas=FigureCanvas(fig)
	png_output = StringIO.StringIO()
	canvas.print_png(png_output)
	response=make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response
 
if __name__ == '__main__':   
	user=sys.argv[1:]
	prof = twitterProfile(user) 
	print prof



