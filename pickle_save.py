import tweepy
import time
import pickle
from tweet_feed import Feed
import datetime

# // AA: Note; 
# //
# // 1 : This is just a quick and inaccurate tool to capture data, acting as a quick hack
# // 2 : run_for_seconds_total % run_for_seconds_break should = 0
# // 3 : There are obvious improvements to be made, for example using datatime or similar to
# //     get accuracy.


# // AA: User options. Note: for accuracy
run_for_seconds_total = 10 
run_for_seconds_break = 5
out_directory = "../DataCollection/"
track = ["from", "cat", "to", "and", "dog" ]


def save_data(_content, _filename):
    pickle_out = open(_filename, "wb")
    pickle.dump(_content, pickle_out)
    pickle_out.close()


def run(sec_total, sec_before_break):
    # // AA: Capture stream
    queue_stream = []
    feed = Feed()
    listener = feed.live_get_listener(queue_stream)
    stream = feed.live_get_streamer(listener, track)

    # // AA: save periodically
    loop_count = sec_total / sec_before_break
    total_runtime = 0
    while loop_count > 0:
        print(f"--- {loop_count} loops remaining")
        countdown_to_slice = sec_before_break
        timpestamp_start = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        while countdown_to_slice > 0:
            countdown_to_slice -= 1
            total_runtime += 1
            print(f"Runtime:{total_runtime} sec, out of {sec_total}")
            time.sleep(1)

        timpestamp_cut = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        filename = f"{out_directory}{timpestamp_start[2:]}--{timpestamp_cut[2:]}" 
        save_data(save_data, filename)
        queue_stream = []
        loop_count -= 1
    stream.disconnect()

if run_for_seconds_total % run_for_seconds_break == 0:
    run(run_for_seconds_total, run_for_seconds_break)
else:
    print("run_for_seconds_total % run_for_seconds_break should be 0!")
print("terminating program")