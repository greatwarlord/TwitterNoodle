import tweepy
import time
import pickle
from tweet_feed import Feed



# // AA: User options
run_for_seconds = 30
out_filename = "pickle_saved_data"
track = ["from", "cat", "to", "and", "dog" ]

# // AA: Capture stream
queue_stream = []
feed = Feed()
listener = feed.live_get_listener(queue_stream)
stream = feed.live_get_streamer(listener, track)

# // AA: After time range; save and terminate
while run_for_seconds > 0:
    run_for_seconds -= 1
    time.sleep(1)

pickle_out = open(out_filename, "wb")
pickle.dump(queue_stream, pickle_out)
pickle_out.close()

stream.disconnect()
print("terminating program")