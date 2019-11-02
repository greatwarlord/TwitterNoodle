import os
import bz2
import pickle 

from random import shuffle # // AA: Testing chronological sorting

# // add support for uncompressed vs compressed

class DatasetScalingHelper():

    directory_out = None
    directory_in = None

    verbosity = False
    fn_format = "YYMMDD-HH_MM_SS--YYMMDD-HH_MM_SS.zip" # // AA: Deprecated
    format_fn_sep = "--"
    format_suffix_zip = ".zip"


    def __init__(self, _verbosity = True):
        self.verbosity = _verbosity

    def check_failsafe(self):
        if self.directory_in is None: self.print_warn("no input dir, aborting"); return False
        if self.directory_out is None: self.print_warn("no output dir, aborting"); return False

        return True

    def print_progress(self, _msg):
        print(f"progress: {_msg}") if self.verbosity else ...

    def print_warn(self, _msg):
        print(f"warn: {_msg}") if self.verbosity else ...

    def set_dir_output(self, _path):
        if not os.path.isdir(_path): self.print_warn("output dir: None. aborting"); return
        if _path[-1] is not "/": _path += "/"
        self.directory_out = _path

    def set_dir_input(self, _path):
        if not os.path.isdir(_path): self.print_warn("input dir: None. aborting"); return
        if _path[-1] is not "/": _path += "/"
        self.directory_in = _path

    def get_file_content(self, _file_name, _is_compressed=True):
        # // implement _is_compressed option (for non compressed alternatives)
        unzipped = bz2.BZ2File(_file_name).read()
        non_binary = pickle.loads(unzipped)
        return non_binary 

    def save_data(self, _content, _path, _compression_enabled):
        if _compression_enabled:
            sfile = bz2.BZ2File(f"{_path}{self.format_suffix_zip}", 'w')
            pickle.dump(_content, sfile)
            sfile.close()
        else:
            pickle_out = open(_path, "wb")
            pickle.dump(_content, pickle_out)
            pickle_out.close()

        self.print_progress(f"saved content to: {_path}{self.format_suffix_zip}")

    def sort_tweetset_chronologically(self, _tweet_list):
        _tweet_list.sort(key=lambda tweet: tweet.created_at, reverse=False)
        self.print_progress("sorted tweet list")
        
    def reformat_tweet_datetime(self, _tweet):      
        dt_string = str(_tweet.created_at)
        dt_string = dt_string = dt_string[2:]
        dt_string = dt_string.replace("-", "")
        dt_string = dt_string.replace(" ", "-")
        dt_string = dt_string.replace(":", "_")
        return dt_string

    def merge_datasets_by_directory(self, _sortby_tweet_time=True):
        if not self.check_failsafe(): return

        file_names = [item[2] for item in os.walk(self.directory_in)]
        #if len(file_names) is 0: self.print_warn("no files detected, aborting") ; return # // hack
        
        undesirables = [".DS_Store"] # // might show up in certain OS. OSX is currently supported
        for x in undesirables:
            try:
                file_names[0].remove(x)
            except:
                pass    

        cache = []
        for name in file_names[0]: cache.extend(self.get_file_content(f"{self.directory_in}{name}"))
        self.sort_tweetset_chronologically(cache)


        new_file_path = ""
        if _sortby_tweet_time:
            filename_start = self.reformat_tweet_datetime(cache[0])
            filename_end = self.reformat_tweet_datetime(cache[-1])
            new_file_path = f"{self.directory_out}{filename_start}{self.format_fn_sep}{filename_end}"
        else:
            # // AA: creates new filename by old filenames, not the same as time attached to tweets.
            filename_start = file_names[0][0].split(self.format_fn_sep)[0]
            filename_end = file_names[0][-1].split(self.format_fn_sep)[1]
            new_file_path = f"{self.directory_out}{filename_start}{self.format_fn_sep}{filename_end}"
            if self.format_suffix_zip in new_file_path:
                new_file_path = new_file_path.split(self.format_suffix_zip)[0]


        print(new_file_path)
        #self.save_data(cache, new_file_path, True)






    def merge_datasets_by_time_range(self):
        pass

    def split_datasets_by_obj_count(self):
        pass

    def split_datasets_by_time_range(self):
        pass


    

s = DatasetScalingHelper()
s.set_dir_output("../TestFolder")
s.set_dir_input("../DataCollection")
s.merge_datasets_by_directory(False)



#p = s.get_file_content("../DataCollection/191101-16_03_06--191101-16_03_11.zip")
#print(p)
# for x in p:
#     print(x.text)

print('terminating')