import tweepy
#import asyncio
import time
import threading
from custom_stream_listener import CustomStreamListener as CSL
from custom_thread import CustomThread
from tweet_feed import Feed
import data_object
from basic_cleaner import BasicCleaner



run_for_seconds = 1
toggle_live = False
dataset_file_path = "../test_set"
track = ["how", "does", "one", "even", "go", "so", "far", "as", "to" ]

queue_stream = []
queue_cleaned = []

stream = None
listener = None



def setup_tweet_stream(out_stream):
    feed = Feed()
    if toggle_live:
        global listener 
        listener = feed.live_get_listener(out_stream)
        global stream 
        stream = feed.live_get_streamer(listener, track)
    else:
        global queue_stream
        queue_stream = feed.disk_get_tweet_queue(dataset_file_path)



def clean_process():
    tweet = queue_stream.pop(0)
    new_data_obj = data_object.get_dataobj_converted(tweet)

    cleaner = BasicCleaner(_text=new_data_obj.text, _auto =True)
    new_data_obj.text = cleaner.get_text_processed()
            
    queue_cleaned.append(new_data_obj)
    
    cleaner.print_comparison()



def cleaner_loop():
    #clean_process()

    while True:
        if len(queue_stream) > 0:
            try:
                clean_process()
            except:
                print("cleaner_loop issue in main.py")



setup_tweet_stream(queue_stream)

first_thread = CustomThread()
first_thread.custom_setup(cleaner_loop, False)
first_thread.start()

    

# // prevent immediate termination
while run_for_seconds > 0:
    run_for_seconds -= 1
    time.sleep(1)


stream.disconnect() if stream is not None else ...
first_thread.stop()
print("terminating program")
