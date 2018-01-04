from tweepy.streaming import StreamListener
from http.client import IncompleteRead
import ssl

from requests.exceptions import Timeout, SSLError
from tweepy import OAuthHandler, API
from tweepy import Stream
import json, time, sys

import tweepy

# Twitter API credentials
consumer_key = "#####################"
consumer_secret = "########################"
access_key = "#########################"
access_secret = "##############################"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
tweets = []


class StdOutListener(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or API()
        self.num_tweets = 0
        super(StdOutListener, self).__init__()

    try:

        def on_data(self, data):

            self.num_tweets += 1
            if self.num_tweets < 20001:
                downloaded_tweets = json.loads(data)
                print(self.num_tweets)
                tweets.append(downloaded_tweets)
                return True
            else:
                print('stopped streaming')
                return False

        def on_error(self, status):
            print('Error on status', status)
            return True

        def on_limit(self, status):
            print('Limit threshold exceeded', status)
            return True

        def on_timeout(self, status):
            print('Stream disconnected; continuing...')
            return True

    except (tweepy.TweepError, SSLError, Timeout, TimeoutError) as e:
        print("Downloaded tweets")
        print("now going to sleep")
        time.sleep(60 * 15)
        print("Woke up")
        time.sleep(60 * 15)
        pass


print('starting streaming')
while True:
    try:
        myStreamListener = StdOutListener()
        mystream = Stream(auth, listener=StdOutListener())
        mystream.filter(track=['#TakeTheKnee', '#TakeAKnee', '#boycottnfl'], languages=["en"])
        if len(tweets) < 20001:
            break
    except Timeout:
        print('time out')
        continue
    except StopIteration:
        break

print('the total downloaded tweets are:' + str(len(tweets)))
with open('C:/Users/srinivas venkatesh/Documents/data science/assignments/assg2/data/data.json', 'w') as file:
    json.dump(tweets, file, sort_keys=True, indent=4)
print('done writting to file')
