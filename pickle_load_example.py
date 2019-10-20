from tweet_feed import Feed



file_path = "../DataCollection/191019-17_45_16--191019-17_45_18"
feed = Feed()
queue_stream = feed.disk_get_tweet_queue(file_path)



for item in queue_stream:
    print(item.text)

print("end of program, terminating..")
