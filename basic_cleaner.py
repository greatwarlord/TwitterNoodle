import nltk
import re

input_from_file = True
file_path = "data_main/data/tweets_txtOnly.txt"

class cleaner_._enum(self):
    def __init__(self):
        pass # // not implemented

class Basic_cleaner(): # // creating bag of words

    # // Note: this class should focus on cleaning data objects ..
    # // instead of fetching files and then -> ..

    # // maybe fever properties, or just use states?

    def __init__(self, _data_raw):
        self.data_raw = _data_raw
        self.data_objects = []
        self.data_objects_cleaned = []

    def set_data(self):
        print("not implemented")
    
    def set_data_tester(self, f_path):
        _load = []
        with open(f_path) as f:
            content = f.read()
            _load = [ row for row in content]
            f.close()
        
        _objects = []
        for item in _load:
            new_data_obj = Data_obj()
            new_data_obj.text = item
            new_data_obj.state = ""
            _objects.append(new_data_obj)

        self.data_objects = objects

    # // < IMPORTANT
    # // the order of cleaning is kinda important. start with complexity? ..
    # // Links first, etc
    # // > important

    def tokenise(self):
        pass
    def detokenise(self):
        pass

    def clean_dates(self):
        pass
    def clean_stopwords(self):
        pass
    def clean_numbers(self)
        pass # // caution: might screw up other cleaners if this is ran first
    def clean_punctuation(self):
        pass # // caution: might screw up other cleaners if this is ran first
    def clean_links(self):
        pass # // re
    def clean_hashtags(self):
        pass # // store?
    def clean_nonsense(self):
        pass # // what & how?
    def clean_named_entities(self):
        pass # // how?
    
    def autoclean(self):
        pass