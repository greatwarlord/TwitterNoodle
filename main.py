import tweepy
#import asyncio
import time
import _thread
import threading
from custom_stream_listener import CustomStreamListener as CSL
from custom_thread import CustomThread
from tweet_feed import Feed
import credentials
import data_object

run_for_seconds = 5
track = ["from", "cat", "to", "and", "dog" ]


queue_stream = []
queue_cleaned = []

feed = Feed()
listener = feed.live_get_listener(queue_stream)
stream = feed.live_get_streamer(listener, track)



def cleaner_loop():
    while True:
        if len(queue_stream) > 0:
            try:
                tweet = queue_stream.pop(0)
                print(tweet.text)

            except:
                pass





first_thread = CustomThread()
first_thread.custom_setup(cleaner_loop, False)
first_thread.start()

    

# // prevent immediate termination
while run_for_seconds > 0:
    run_for_seconds -= 1
    time.sleep(1)

stream.disconnect()
first_thread.stop()
print("terminating program")
