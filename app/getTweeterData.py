# tweepy is used to call the Twitter API from Python
import tweepy
import re
import csv
import os
from random import shuffle


# This is the twitter user that we will be profiling using our news classifier.
#TWITTER_USER = 'raulgarreta'
TWITTER_USER = 'amr_i_hamed'

#Get user twitter data
def get_friends_descriptions(api, twitter_account, max_users=100):
    """
    Return the bios of the people that a user follows
    
    api -- the tweetpy API object
    twitter_account -- the Twitter handle of the user
    max_users -- the maximum amount of users to return
    """
    
    user_ids = api.friends_ids(twitter_account)
    shuffle(user_ids)
    
    following = []
    for start in xrange(0, min(max_users, len(user_ids)), 100):
        end = start + 100
        following.extend(api.lookup_users(user_ids[start:end]))
    
    descriptions = []
    for user in following:
        description = re.sub(r'(https?://\S+)', '', user.description.encode("utf-8"))

        # Only descriptions with at least ten words.
        if len(re.split(r'[^0-9A-Za-z]+', description)) > 10:
            descriptions.append(description.strip('#').strip('@'))
    
    
    return descriptions


def get_tweets(api, twitter_user, tweet_type='timeline', max_tweets=200, min_words=5):
    
    tweets = []
    
    full_tweets = []
    step = 200  # Maximum value is 200.
    for start in xrange(0, max_tweets, step):
        end = start + step
        
        # Maximum of `step` tweets, or the remaining to reach max_tweets.
        count = min(step, max_tweets - start)

        kwargs = {'count': count}
        if full_tweets:
            last_id = full_tweets[-1].id
            kwargs['max_id'] = last_id - 1

        if tweet_type == 'timeline':
            current = api.user_timeline(twitter_user, **kwargs)
        else:
            current = api.favorites(twitter_user, **kwargs)
        
        full_tweets.extend(current)
    
    for tweet in full_tweets:
        text = re.sub(r'(https?://\S+)', '', tweet.text)
        
        score = tweet.favorite_count + tweet.retweet_count
        if tweet.in_reply_to_status_id_str:
            score -= 15

        # Only tweets with at least five words.
        if len(re.split(r'[^0-9A-Za-z]+', text)) > min_words:
            tweets.append((text, score))
            
    return tweets


def get_all_tweets(screen_name, tweet_type='timeline',min_words=5):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#initialize a list to hold all the tweepy Tweets
    alltweets = []	
	
    if tweet_type == 'timeline':
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    else:
    	#make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.favorites(screen_name = screen_name,count=200)
	
	#save most recent tweets
    alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, include_entities=True)
		
		#save most recent tweets
        alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
		
        print "...%s tweets downloaded so far" % (len(alltweets))		
	
	#print tweets
	#transform the tweepy tweets into a 2D array that will populate the csv
    for tweet in alltweets:
        text = re.sub(r'(https?://\S+)', '', tweet.text)
        score = tweet.favorite_count + tweet.retweet_count
        if tweet.in_reply_to_status_id_str:
            score -= 15

        # Only tweets with at least five words.
        if len(re.split(r'[^0-9A-Za-z]+', text)) > min_words:
            tweets.append((text.encode("utf-8"), score))
	
    return tweets


if __name__ == '__main__':   
   

    # TWITTER SETTINGS
    # Put here your credentials to consume Twitter API
    TWITTER_CONSUMER_KEY= os.environ['consumer_key']
    TWITTER_CONSUMER_SECRET= os.environ['consumer_secret']
    TWITTER_ACCESS_TOKEN_KEY= os.environ['access_key']
    TWITTER_ACCESS_TOKEN_SECRET= os.environ['access_secret']

    # Authenticate to Twitter API
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

	# Get the descriptions of the people that twitter_user is following.
    descriptions = []
    descriptions.extend(get_friends_descriptions(api, TWITTER_USER, max_users=300))
    
    with open('%s_description.csv' % TWITTER_USER, 'wb') as f:
        writer = csv.writer(f)
        for desc in descriptions:
            writer.writerow([desc]) 

      #  print descriptions

    tweets = []
    tweets.extend(get_all_tweets(TWITTER_USER, 'timeline',5))
    tweets.extend(get_all_tweets(TWITTER_USER, 'favorites',5))
    
        #write the csv    
    with open('%s_tweets.csv' % TWITTER_USER, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(tweets)