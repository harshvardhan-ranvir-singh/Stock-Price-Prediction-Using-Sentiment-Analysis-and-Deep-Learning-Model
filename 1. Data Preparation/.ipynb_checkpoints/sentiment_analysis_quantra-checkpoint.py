# -*- coding: utf-8 -*-
"""
@author: Quantra
"""
import pandas as pd
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# API key to access tweepy
def get_twitter_tokens():
    # To get Twitter API keys, follow the steps given in the 'Get Twitter API Keys - Guide.pdf'
    # This PDF is available under the Section 3, Unit 2 in the course
    return {
                    'consumer_key':"Copy your consumer key here",
                    'consumer_secret':"Copy your consumer secret here here",
                    'access_token':"Copy your access token here",
                    'access_token_secret':"Copy your access token secret here",
    }    

# API key to access Botometer
def get_rapid_api_key():
    # To get Rapid API key follow the steps given in the 'Get Botometer API Key - Guide.pdf'
    # This PDF is available under the Section 7, Unit 2 in the course
    # Create an account in the following link and get the API key
    # Link: https://rapidapi.com/OSoMe/api/botometer?utm_source=mashape&utm_medium=301
    return "Copy your Botometer API key here"
  
# API key to access Webhoseio
def get_webhoseio_key():
    # To get API key for webhoseio follow the steps given in the 'S12 Fetching news articles.ipynb' under 'Getting API key'
    # These Steps are available under the Section 12, Unit 5 in the course
    return "Copy your Webhoseio API key here"

# This function returns API object
def get_tweepy_api():
    # Get the Twitter tokens
    twitter_tokens = get_twitter_tokens()
    consumer_key = twitter_tokens['consumer_key']
    consumer_secret = twitter_tokens['consumer_secret']
    # Create authentication object
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    return api

# This function returns tweet objects
def get_tweet_objects_from_id(tweet_id_list):
    tweet_list = []
    # Get the API object
    api = get_tweepy_api()
    # Fetch the list of tweet objects
    for i in range(0,len(tweet_id_list),100):
        tweet_list = tweet_list + (api.statuses_lookup(tweet_id_list[i:(100+i)], tweet_mode = 'extended'))
    
    return tweet_list

# This function returns the text of the tweet object
def get_tweet_text(tweet_object):
    return tweet_object.full_text

# This function returns the ID of the tweet object
def get_tweet_id(tweet_object):
    return tweet_object.id_str

# This function returns the retweet count of the tweet object
def get_retweet_count(tweet_object):
    return tweet_object.retweet_count

# This function returns the created date of the tweet object
def get_tweet_date(tweet_object):
    return tweet_object.created_at

# This function returns the username of the tweet object
def get_tweet_username(tweet_object):
    return tweet_object.user.screen_name

# This function returns the compound score calculated by VADER of the tweet
analyzer = SentimentIntensityAnalyzer()
def get_VADER_score(tweet):
    return analyzer.polarity_scores(tweet)['compound']

# Import datetime and timedelta from datetime package
from datetime import datetime, timedelta
until_date = (datetime.now()+timedelta(1)).strftime("%Y-%m-%d")
since_date = (datetime.now()-timedelta(1)).strftime("%Y-%m-%d")

# This function fetches the required tweet information using tweepy Cursor
def get_tweet_details_by_query(query, since=since_date, until=until_date):
    api = get_tweepy_api()
    # Using the cursor method to fetch the tweets using api.search method
    cursor_result = tweepy.Cursor(api.search, q=query, since=since_date, until=until_date, count = 100)
    all_tweets = cursor_result.items()
    tweets_df = pd.DataFrame()
    for tweet in all_tweets:
        tweets_df = tweets_df.append(
                                        {
                                            'Tweet ID': tweet.id_str,
                                            'Created At': tweet.created_at,
                                            'User Screen Name': tweet.user.screen_name,
                                            'Tweet Text': tweet.text,
                                            'Retweet Count': tweet.retweet_count,
                                            'Favourite Count': tweet.favorite_count,
                                            'Language': tweet.lang,   
                                        },
                                        ignore_index=True    
        )
    return tweets_df

#This function returns a dictionary of the required tweet information
def get_tweet_details_by_id(tweet_id_list):
    tweet_list = get_tweet_objects_from_id(tweet_id_list)
    tweets = pd.DataFrame()
    tweets['tweet_object'] = tweet_list
    tweets['tweet_text'] = tweets['tweet_object'].apply(get_tweet_text)
    tweets['tweet_username'] = tweets['tweet_object'].apply(get_tweet_username)
    tweets['tweet_id'] = tweets['tweet_object'].apply(get_tweet_id)
    tweets['retweet_count'] = tweets['tweet_object'].apply(get_retweet_count)
    tweets['created_date'] = tweets['tweet_object'].apply(get_tweet_date) 
    
    return tweets[["tweet_id", "created_date", "tweet_username", "tweet_text", "retweet_count"]]