import pickle
from tweet_feed import Feed



file_path = "../DataCollection/191013-20_19_45--191013-20_19_50"
feed = Feed()
queue_stream = feed.disk_get_tweet_queue(file_path)



for item in queue_stream:
    print(item.text)



print("end of program, terminating..")



l = [x.text for x in queue_stream]