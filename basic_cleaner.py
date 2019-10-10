import nltk
import re



class CleanerEnum(self):
    def __init__(self):
        pass

class BasicCleaner():


    def __init__(self, _text, _destination):
        self.text_raw = _text
        self.text_processed = None
        self.destination = _destination

    def pass_along_data(self):
        self.destination.append(self.text_processed)
    
 
    def tokenise(self):
        pass
    def detokenise(self):
        pass

    def clean_dates(self):
        pass
    def clean_stopwords(self):
        pass
    def clean_numbers(self)
        pass
    def clean_punctuation(self):
        pass
    def clean_links(self):
        pass
    def clean_hashtags(self):
        pass
    def clean_nonsense(self):
        pass
    def clean_named_entities(self):
        pass
    
    def autoclean(self):
        pass