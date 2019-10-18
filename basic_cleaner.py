
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer 
import re
import string
from textblob import TextBlob as TB


# class CleanerEnum(self):
#     def __init__(self):
#         pass

class BasicCleaner():

    def __init__(self, _text, _auto):
        self.text_raw = _text
        self.text_processed = ""
        self.filtered_hashtag = []
        self.filtered_alphatag = []
        self.sentiment = False
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
        print(f"sentiment:{self.sentiment}")
        #print(f"hashtags: {self.filtered_hashtag}")
        print("--------end new-----------")
        print("##########################")

    def autocleaner(self):
        #self.text_processed = self.text_raw
        no_link = self.clean_links(self.text_raw)
        no_hashtag = self.clean_hashtags(no_link)
        no_alphatags = self.clean_alphatag(no_hashtag)
        no_punct = self.clean_punctuation(no_alphatags)
        tokens = self.tokenise(no_punct)
        wo_stop = self.clean_stopwords(tokens)
        de_tokens = self.detokenise(wo_stop)

        self.text_processed = de_tokens
        self.set_sentiment(de_tokens, float(0))
 
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
        return re.sub(r"[a-z]*[:.]+\S+","",text_in)

    def clean_hashtags(self, text_in):
        self.filtered_hashtag = (re.findall(r"[#]\S*", text_in))
        return re.sub(r"[#]\S*", "", text_in)

    def clean_alphatag(self, text_in):
        self.filtered_alphatag = (re.findall(r"[@]\S*", text_in))
        return re.sub(r"[@]\S*", "", text_in)

    def clean_nonsense(self):
        pass
    def clean_named_entities(self):
        pass
    
    def clean_convert_to_lowercase(self):
        pass

    def set_sentiment(self, text_in, threshold):
        if TB(text_in).sentiment[0] > threshold:
            self.sentiment = True
        else:
            self.sentiment = False
        