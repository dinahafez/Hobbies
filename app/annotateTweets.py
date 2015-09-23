# tweepy is used to call the Twitter API from Python
import tweepy
import re
import csv
from random import shuffle
import os

# TWITTER SETTINGS
# Put here your credentials to consume Twitter API
TWITTER_CONSUMER_KEY= os.environ['consumer_key']
TWITTER_CONSUMER_SECRET= os.environ['consumer_secret']
TWITTER_ACCESS_TOKEN_KEY= os.environ['access_key'],
TWITTER_ACCESS_TOKEN_SECRET= os.environ['access_secret']

# This is the twitter user that we will be profiling using our news classifier.
#TWITTER_USER = 'raulgarreta'
TWITTER_USER = 'amr_i_hamed'

# MONKEYLEARN SETTINGS
# Put here your MonkeyLearn API token
MONKEYLEARN_TOKEN = os.environ['monkeyLearn_token']

MONKEYLEARN_CLASSIFIER_BASE_URL = 'https://api.monkeylearn.com/api/v1/categorizer/'
MONKEYLEARN_EXTRACTOR_BASE_URL = 'https://api.monkeylearn.com/api/v1/extraction/'

# This classifier is used to detect the tweet/bio's language
MONKEYLEARN_LANG_CLASSIFIER_ID = 'cl_hDDngsX8'

# This classifier is used to detect the tweet/bio's topics
MONKEYLEARN_TOPIC_CLASSIFIER_ID = 'cl_5icAVzKR' #cl_hS9wMk9y'#

# This extractor is used to extract keywords from tweets and bios
MONKEYLEARN_EXTRACTOR_ID = 'ex_y7BPYzNG'

#Detect language with MonkeyLearn API
import requests
import json

# This is a handy function to classify a list of texts in batch mode (much faster)
def classify_batch(text_list, classifier_id):
    """
    Batch classify texts
    text_list -- list of texts to be classified
    classifier_id -- id of the MonkeyLearn classifier to be applied to the texts
    """
    results = []
    
    step = 250
    for start in xrange(0, len(text_list), step):
        end = start + step

        data = {'text_list': text_list[start:end]}

        response = requests.post(
            MONKEYLEARN_CLASSIFIER_BASE_URL + classifier_id + '/classify_batch_text/',
            data=json.dumps(data),
            headers={
                'Authorization': 'Token {}'.format(MONKEYLEARN_TOKEN),
                'Content-Type': 'application/json'
        })
        
        try:
            results.extend(response.json()['result'])
        except:
            print response.text
            raise

    return results

def filter_language(texts, language='English'):
    
    # Get the language of the tweets and bios using Monkeylearn's Language classifier
    lang_classifications = classify_batch(texts, MONKEYLEARN_LANG_CLASSIFIER_ID)
    
    # Only keep the descriptions that are writtern in English.
    lang_texts = [
        text
        for text, prediction in zip(texts, lang_classifications)
        if prediction[0]['label'] == language
    ]

    return lang_texts


from collections import Counter

def category_histogram(texts, short_texts):
    
    # Classify the bios and tweets with MonkeyLearn's news classifier.
    topics = classify_batch(texts, MONKEYLEARN_TOPIC_CLASSIFIER_ID)
    
    # The histogram will keep the counters of how many texts fall in
    # a given category.
    histogram = Counter()
    samples = {}

    for classification, text, short_text in zip(topics, texts, short_texts):

        # Join the parent and child category names in one string.
        category = classification[0]['label']
        probability = classification[0]['probability']
        
        if len(classification) > 1:
            category += '/' + classification[1]['label']
            probability *= classification[1]['probability']
        
        MIN_PROB = 0.0
        # Discard texts with a predicted topic with probability lower than a treshold
        if probability < MIN_PROB:
            continue
        
        # Increment the category counter.
        histogram[category] += 1
        
        # Store the texts by category
        samples.setdefault(category, []).append((short_text, probability))
        
    return histogram, samples

if __name__ == '__main__':   
    tweets=[]
    descriptions=[]
    
    with open('%s_tweets.csv' % TWITTER_USER, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tweets.append(row)
            
        
    #filter to only keep tweets in English
    tweets_english = filter_language(tweets)
    print "Tweets found: {}".format(len(tweets_english))
    
      # Classify the expanded tweets using MonkeyLearn, return the historgram
    tweets_histogram, tweets_categorized = category_histogram(tweets_english, tweets_english)

    # Print the categories sorted by most frequent
    for topic, count in tweets_histogram.most_common():
        print count, topic

    with open('%s_tweets_histogram.csv' % TWITTER_USER, 'wb') as f:
        for k,v in  tweets_histogram.most_common():
            f.write( "{} ,{}\n".format(k,v) )
            
    with open('%s_tweets_categorized.csv' % TWITTER_USER, 'wb') as f:
        json.dump(tweets_categorized, f)


#######read####
    tweets_read=Counter()
    with open('%s_tweets_histogram.csv' % TWITTER_USER, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tweets_read[row[0]]= int(row[1])
            print row[1]
    for topic, count in tweets_read.most_common():
        print topic, count
        
    with open('%s_tweets_categorized.csv' % TWITTER_USER) as data_file:    
        data = json.load(data_file)

##################

    with open('%s_description.csv' % TWITTER_USER, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            descriptions.append(row)
    
    descriptions_english = filter_language(descriptions)
    print "Descriptions found: {}".format(len(descriptions_english))
    
    # Classify the expanded bios of the followed users using MonkeyLearn, return the historgram
    descriptions_histogram, descriptions_categorized = category_histogram(descriptions_english, descriptions_english)

    # Print the catogories sorted by most frequent
    for topic, count in descriptions_histogram.most_common():
        print count, topic
    

    with open('%s_description_histogram.csv' % TWITTER_USER, 'wb') as f:
        for k,v in  descriptions_histogram.most_common():
            f.write( "{} ,{}\n".format(k,v) )
            
    with open('%s_description_categorized.csv' % TWITTER_USER, 'wb') as f:
        json.dump(descriptions_categorized, f)
 
    