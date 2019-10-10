import tweepy
#import asyncio
import time
import _thread
import threading
from custom_stream_listener import CustomStreamListener as CSL
from custom_thread import CustomThread
import credentials
import data_object



listener = None
stream = None
track = ["from", "cat", "to", "and", "dog" ]

queue_stream = []
queue_cleaned = []



def live_stream_setup():
    auth = credentials.auth
    api = tweepy.API(auth)
    api.wait_on_rate_limit = True
    api.wait_on_rate_limit_notify = True

    global listener
    listener = CSL()
    global queue_stream
    listener.custom_setup(_destination = queue_stream,      \
                                _stream_toggle = True,      \
                                    _warn_verbosity = True)

    global stream
    stream = tweepy.Stream(auth = auth, listener=listener)
    stream.filter(track=track, languages=["en"], is_async= True)
    
    print("setup complete")





def cleaner_loop():
    while True:
        if len(queue_stream) > 0:
            try:
                tweet = queue_stream.pop(0)
                print(tweet.text)

            except:
                pass








live_stream_setup()

first_thread = CustomThread()
first_thread.custom_setup(cleaner_loop, False)
first_thread.start()

    

# // prevent termination
while True:
    time.sleep(1)


# stream.disconnect()
# print("terminating program")
