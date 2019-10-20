# // AA: IMPORTANT: This script is a hack for capturing some data. It is neither robust nor accurate.
import tweepy
import time
import pickle
from tweet_feed import Feed
import datetime
import bz2
from custom_thread import CustomThread



# // AA: Handles
run_for_seconds_total = 10 
run_for_seconds_break = 10
out_directory = "../DataCollection/"
zip_enabled = False
track = ["from", "cat", "to", "and", "dog" ]



def save_data(_content, _filename):
    content_copy = _content.copy()
    def save():
        if zip_enabled:
            sfile = bz2.BZ2File(f"{_filename}.zip", 'w')
            pickle.dump(content_copy, sfile)
            sfile.close()
            print(f"len:{len(content_copy)}")
        else:
            pickle_out = open(_filename, "wb")
            print(f"len:{len(content_copy)}")
            pickle.dump(content_copy, pickle_out)
            pickle_out.close()

    first_thread = CustomThread(save, False) # // AA: DO NOT CHANGE TO TRUE!
    first_thread.start()



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
        timpestamp_start = datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")
        while countdown_to_slice > 0:
            countdown_to_slice -= 1
            total_runtime += 1
            print(f"Runtime:{total_runtime} sec, out of {sec_total}")
            time.sleep(1)

        timpestamp_cut = datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")
        filename = f"{out_directory}{timpestamp_start[2:]}--{timpestamp_cut[2:]}" 
        save_data(queue_stream, filename)
        queue_stream.clear()
        
        loop_count -= 1
    stream.disconnect()



if run_for_seconds_total % run_for_seconds_break == 0:
    if run_for_seconds_total >= run_for_seconds_break: # // AA: hack
        run(run_for_seconds_total, run_for_seconds_break)
    else: 
        print("total runtime is lower than slice interval. Aborting")
else:
    print("run_for_seconds_total % run_for_seconds_break should be 0!")
print("terminating program")