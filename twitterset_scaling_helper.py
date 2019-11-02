import os
import bz2
import pickle 

# // add support for uncompressed vs compressed

class DatasetScalingHelper():

    out_directory = None
    verbosity = False
    fn_format = "YYMMDD-HH_MM_SS--YYMMDD-HH_MM_SS.zip"
    format_suffix_zip = ".zip"

    def __init__(self, _verbosity = True):
        self.verbosity = _verbosity

    def check_failsafe(self):
        pass

    def print_progress(self, _msg):
        print(f"progress: {_msg}") if self.verbosity else ...

    def print_warn(self, _msg):
        print(f"warn: {_msg}") if self.verbosity else ...

    def set_out_dir(self, _path):
        if not os.path.isdir(_path): self.print_warn("input dir: None. aborting") ; return
        if _path[-1] is not "/": _path += "/"
        self.out_directory = _path

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

    def merge_datasets_by_directory(self, _in_dir, _start_end_seperator):
        if not os.path.isdir(_in_dir): self.print_warn("input dir: None. aborting"); return
        if _in_dir[-1] is not "/": _in_dir += "/"

        file_names = [item[2] for item in os.walk(_in_dir)]
        #if len(file_names) is 0: self.print_warn("no files detected, aborting") ; return # // hack
        
        undesirables = [".DS_Store"] # // might show up in certain OS. OSX is currently supported
        #if ".DS_Store" in file_names[0]: file_names[0].remove(".DS_Store")
        for x in undesirables:
            try:
                file_names[0].remove(x)
            except:
                pass    

        #cache = [self.get_file_content(f"{_in_dir}{name}") for name in file_names[0]]
        cache = []
        for name in file_names[0]:
            #cache.append(self.get_file_content(f"{_in_dir}{name}"))
            cache.extend(self.get_file_content(f"{_in_dir}{name}"))
        
            
        print(cache[0].created_at)

        # for item in cache:
        #     print(item.created_at)    


        # // AA: Get new filename and save
        first_file_start = file_names[0][0].split(_start_end_seperator)[0]
        last_file_end = file_names[0][-1].split(_start_end_seperator)[1]
        new_name = f"{first_file_start}{_start_end_seperator}{last_file_end}"
        if self.format_suffix_zip in new_name:  new_name = new_name.split(self.format_suffix_zip)[0]
        #print(f"new path: {self.out_directory}{new_name}")
    
        #self.save_data(cache, f"{self.out_directory}{new_name}", True)



        
        


    def merge_datasets_by_time_range(self):
        pass

    def split_datasets_by_obj_count(self):
        pass

    def split_datasets_by_time_range(self):
        pass

out_dir = "../TestFolder"
in_dir = "../DataCollection"
s = DatasetScalingHelper()
s.set_out_dir(out_dir)
s.merge_datasets_by_directory(in_dir, "--")



#p = s.get_file_content("../DataCollection/191101-16_03_06--191101-16_03_11.zip")
#print(p)
# for x in p:
#     print(x.text)

print('terminating')