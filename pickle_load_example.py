import pickle
from tweet_feed import Feed

file_path = "pickle_saved_data"
feed = Feed()
queue_stream = feed.disk_get_tweet_queue(file_path)


for item in queue_stream:
    print(item.text)





