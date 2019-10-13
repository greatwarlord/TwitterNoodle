
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer 
import re
import string



# class CleanerEnum(self):
#     def __init__(self):
#         pass

class BasicCleaner():

    def __init__(self, _text, _auto):
        self.text_raw = _text
        self.text_processed = ""
        if _auto:
            self.autocleaner()

    def get_text_processed(self):
        return self.text_processed

    def print_comparison(self):
        print("##########################")
        print("-------start raw----------")
        print(self.text_raw)
        print("--------end raw-----------")
        print("-------start new----------")
        print(self.text_processed)
        print("--------end new-----------")
        print("##########################")

    def autocleaner(self):
        #self.text_processed = self.text_raw
        no_link = self.clean_links(self.text_raw)
        no_punct = self.clean_punctuation(no_link)
        tokens = self.tokenise(no_punct)
        wo_stop = self.clean_stopwords(tokens)
        de_tokens = self.detokenise(wo_stop)

        self.text_processed = de_tokens
 
    def tokenise(self, text_in):
        return word_tokenize(text_in) 

    def detokenise(self, tokens):
        return TreebankWordDetokenizer().detokenize(tokens)

    def clean_dates(self):
        pass
    def clean_stopwords(self, text_in):
        stop_words = set(stopwords.words('english')) 
        return [item for item in text_in if not item in stop_words] 

    def clean_numbers(self):
        pass

    def clean_punctuation(self, text_in):
        return text_in.translate(str.maketrans('', '', string.punctuation))

    def clean_links(self, text_in):
        return re.sub(r"[a-z]*[:.]+\S+", "",text_in)

    def clean_hashtags(self):
        pass
    def clean_nonsense(self):
        pass
    def clean_named_entities(self):
        pass
    
    def autoclean(self):
        pass