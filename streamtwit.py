from __future__ import absolute_import, print_function

import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
from twitlogin import *
import datetime


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import threading


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just writes received tweets to stdout.

    """

    def __init__(self, path):
        self.tweets_data_path = path



    def on_data(self, data):
        #print(data)
        #tweet = data.split(',"text":"')[1].split('","source":"')[0]
        savefile = open( self.tweets_data_path, 'a') #was ab
        savefile.write(data)
        savefile.close()
        return True

    def on_error(self, status):
        print(status)

    def on_disconnect(self):
        return False


'''if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    streamdata = stream.filter(track=['@magnetar1']) #Can also use things like locations=[-74.0231,45.3299,-73.3846,45.7311]
            '''

class TwitData(): #class for reading and formatting twitter data

    #reads data from file and tells you if something goes wrong
    def readTwitFile(self, tweets_data_path):
        self.tweets_data_path = tweets_data_path

        self.tweets_data = []
        self.tweets_file = open(self.tweets_data_path, "r")
        for line in self.tweets_file:
            try:
                self.tweet = json.loads(line)
                self.tweets_data.append(self.tweet)
            except:
                print('failure')
                continue

        #self.tweets = pd.DataFrame()
        #self.tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
        #self.tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
        #self.tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

        #return(self.tweets)

        return(self.tweets_data)
    #puts the files in nice format from pandas package
    def formatTwitData(self, tweets_data):
        self.tweets_data = tweets_data

        self.tweets = pd.DataFrame()
        self.tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
        self.tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
        self.tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

        return(self.tweets)
#class that contains many functions for scraping
class TwitScrape():
    #scrapes twitter for certain keywords. Needs a path to store the file, the dates
    # where it has to do the scraping and the amount of items you want to search(0 is all)
    def scrapeKeyword(self, keyword, tweets_data_path, until = 'none', since = ' ', language = 'en', items = 0):
        self.keyword = keyword
        self.tweets_data_path = tweets_data_path

        if until == 'none':
            self.current = datetime.datetime.now()
            self.until = str(self.current.year)  +'-' +  str(self.current.month) + '-' + str(self.current.day)
        else:
            self.until = until

        self.since = since
        self.language = language
        self.items = items
        #print('changes have been made')

        api = tweepy.API(twitLogin())
        self.tweets_data = []
        savefile = open( self.tweets_data_path, 'ab')
        for tweet in tweepy.Cursor(api.search, q = self.keyword ,since= self.since, until = self.until ,lang= self.language).items(self.items):
            savefile.write(json.dumps(tweet._json)) #converts the tweet to json and then write it.
            self.tweets_data.append(json.dumps(tweet._json))

        savefile.close()

        return(self.tweets_data)
    #finds all the users tweets
    def scrapeUsertweets(self, items = 0):
        self.api = tweepy.API(twitLogin())
        self.user_tweets = []
        self.items = items

        for status in tweepy.Cursor(self.api.home_timeline).items(self.items):
            # Process a single status
            self.user_tweets.append(status)

        return(self.user_tweets)
    #gives a list of who the user is following
    def followingList(self, items = 0):
        self.api = tweepy.API(twitLogin())
        self.following_list = []
        self.items = items
        for friend in tweepy.Cursor(self.api.friends).items(self.items):
            self.following_list.append(friend)

        return(self.following_list)