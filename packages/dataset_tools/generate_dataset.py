import time
from datetime import datetime
import bz2
import pickle

from packages.feed.tweet_feed import Feed
from packages.misc.custom_thread import CustomThread as CustomThread

from packages.cleaning import custom_stopwords



class Generate_Dataset():

    is_running = False
    timestamp_start = None
    runtime_total = None
    runtime_between_slices = None
    runtime_forever = False
    
    out_directory = None
    out_filename_format = "%Y%m%d-%H_%M_%S" # // AA: For datetime
    zipping_enabled = True

    abort_queued = False
    verbosity = False

    track_keywords = None



    def __init__(self, _runtime_total, 
                        _runtime_between_slices, 
                            _runtime_forever, 
                                _out_directory, _track_keywords):
        self.runtime_total = _runtime_total
        self.runtime_between_slices = _runtime_between_slices
        self.runtime_forever = _runtime_forever
        self.out_directory = _out_directory
        self.track_keywords = _track_keywords


    def print_progress(self, _content):
        if not self.verbosity: return
        # // AA: Hook to interface?
        print(f"{_content}")


    def print_progress_bar(self, _current,_max, _bar_size = 20, _descriptor="", leave_last=True):
        # // AA: guard divide by zero
        percent = 0
        try: percent = float(_current) / float(_max) * float(100)
        except: pass
        # // AA: Setup
        depict_arr = "="
        depict_empty = " "
        bar_progress = int((percent / 100 ) * _bar_size)
        empty_count = int(_bar_size - bar_progress)
        bar_str = f" |{depict_arr*bar_progress}>{depict_empty*empty_count}| {round(percent, 1)}%"
        print(f"{' '*100}", end="\r") # // AA: bad hack
        # // AA: Execute
        if bar_progress is _bar_size and leave_last: print(f"{_descriptor} {bar_str}")
        else: print(f"{_descriptor} {bar_str}", end="\r")


    def validate_session(self):
        if self.runtime_total is None: return False
        if self.runtime_between_slices is None: return False
        if self.runtime_total % self.runtime_between_slices is not 0: return False
        if not self.runtime_forever and self.runtime_between_slices > self.runtime_total: return False
        if self.out_directory is None: return False
        if self.track_keywords is None: return False 
        
        return True


    def get_time_left(self):
        if not self.is_running: return "Not running"
        if self.runtime_forever: return "Undefined, running forever"
        if not self.validate_session(): return "session not valid"
        return self.runtime_total - (int(time.mktime(datetime.now().timetuple())) - self.timestamp_start)


    def save_data(self, _content, _filename):
        content_copy = _content.copy()
        def save():
            if self.zipping_enabled:
                sfile = bz2.BZ2File(f"{_filename}.zip", 'w')
                pickle.dump(content_copy, sfile)
                sfile.close()
            else:
                pickle_out = open(_filename, "wb")
                pickle.dump(content_copy, pickle_out)
                pickle_out.close()

        first_thread = CustomThread(save, False) # // AA: DO NOT CHANGE TO TRUE!
        first_thread.start()


    def run_collector(self):
        if not self.validate_session():
            print("session not valid, aborting")
            return

        # // AA: Setup stream
        queue_stream = []
        feed = Feed()
        listener = feed.live_get_listener(queue_stream)
        stream = feed.live_get_streamer(listener, self.track_keywords)

        # // AA: Setup time
        self.is_running = True
        time_current = int(time.mktime(datetime.now().timetuple()))
        self.timestamp_start = time_current
        time_end = time_current + self.runtime_total
        time_next_slice = time_current + self.runtime_between_slices
        filename_timestamp_last = datetime.now().strftime(self.out_filename_format)

        # // AA: Run
        while time_end > time_current or self.runtime_forever:
            if self.abort_queued: print("aborting collector.."); break
            time_current = int(time.mktime(datetime.now().timetuple()))

            # // AA: Save on slice
            if time_current >= time_next_slice :
                time_next_slice = time_current + self.runtime_between_slices
                filename_timestamp_new = datetime.now().strftime(self.out_filename_format)
                filename = f"{self.out_directory}{filename_timestamp_last[2:]}--{filename_timestamp_new[2:]}" 
                self.save_data(queue_stream, filename)
                filename_timestamp_last = datetime.now().strftime(self.out_filename_format)
                self.print_progress(f"making slice, count: {len(queue_stream)}")
                queue_stream.clear()

            self.print_progress_bar((time_current - self.timestamp_start), self.runtime_total,20,  f"time remaining: {self.get_time_left()}")
                
        # // AA: End
        stream.disconnect()
        self.is_running = False


def test(_path="../DataCollection/", _time_total=10, _time_between_slices=10, _track=None ):
    run_forever = False
    if _track is None:
        _track = custom_stopwords.main()

    gen = Generate_Dataset(_time_total, _time_between_slices, run_forever, _path, _track)
    gen.run_collector()

    print("terminated")