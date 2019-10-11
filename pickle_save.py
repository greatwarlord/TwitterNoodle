import tweepy
import time
import pickle
from tweet_feed import Feed
import datetime


# // AA: User options
run_for_seconds_total = 30
run_for_seconds_break = 10
out_filename = "../test_set"
track = ["from", "cat", "to", "and", "dog" ]

# // AA: Capture stream
queue_stream = []
feed = Feed()
listener = feed.live_get_listener(queue_stream)
stream = feed.live_get_streamer(listener, track)

# // AA: ToDo: create use timestamp for file naming.
# // AA: ToDo: partition each seconds into smaller files for memory friendliness.
# // AA: ToDo: Use datetime to datermine runtime instead of decrementation of run_for_seconds
#timpestamp_start = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


# // AA: After time range; save and terminate
while run_for_seconds_total > 0:
    run_for_seconds_total -= 1
    time.sleep(1)
    print(f"time left before program saves and terminates: {run_for_seconds_total}")

pickle_out = open(out_filename, "wb")
pickle.dump(queue_stream, pickle_out)
pickle_out.close()

stream.disconnect()
print("terminating program")