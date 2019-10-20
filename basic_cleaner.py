
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer 
import re
import string
from textblob import TextBlob as TB





class BasicCleaner():



    @staticmethod
    def print_comparison(_data_obj, _text_raw):
        print("##########################")
        print("-------start raw----------")
        print(_text_raw)
        print("--------end raw-----------")
        print("-------start new----------")
        print(_data_obj.text)
        print(f"sentiment:{_data_obj.valid_sentiment_range}")
        print(f"hashtags: {_data_obj.hashtags}")
        print(f"alphatags: {_data_obj.alphatags}")
        print("--------end new-----------")
        print("##########################")

    @classmethod
    def autocleaner(self, _data_obj, _sentiment_range, _verbosity):

        text_raw = _data_obj.text
        self.clean_links(_data_obj)
        self.clean_hashtags(_data_obj)
        self.clean_alphatags(_data_obj)
        self.clean_punctuation(_data_obj)
        self.tokenise(_data_obj)
        self.clean_stopwords(_data_obj)
        self.detokenise(_data_obj)
        self.set_sentiment(_data_obj, _sentiment_range)

        if _verbosity:
            self.print_comparison(_data_obj, text_raw)
 
    @staticmethod
    def tokenise(_data_obj):
        _data_obj.text = word_tokenize(_data_obj.text)

    @staticmethod
    def detokenise(_data_obj):
        _data_obj.text = TreebankWordDetokenizer().detokenize(_data_obj.text)

    @staticmethod
    def clean_dates(_data_obj):
        pass

    @staticmethod
    def clean_stopwords(_data_obj):
        stop_words = set(stopwords.words('english')) 
        _data_obj.text = [item for item in _data_obj.text if not item in stop_words] 

    @staticmethod
    def clean_numbers(_data_obj):
        pass

    @staticmethod
    def clean_punctuation(_data_obj):
        _data_obj.text = _data_obj.text.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def clean_links(_data_obj):
        _data_obj.text = re.sub(r"[a-z]*[:.]+\S+","",_data_obj.text)

    @staticmethod
    def clean_hashtags(_data_obj):
        _data_obj.hashtags = (re.findall(r"[#]\S*", _data_obj.text))
        _data_obj.text = re.sub(r"[#]\S*", "", _data_obj.text)

    @staticmethod
    def clean_alphatags(_data_obj):
        _data_obj.alphatags = (re.findall(r"[@]\S*", _data_obj.text))
        _data_obj.text = re.sub(r"[@]\S*", "", _data_obj.text)

    @staticmethod
    def clean_nonsense(_data_obj):
        pass

    @staticmethod
    def clean_named_entities(_data_obj):
        pass

    @staticmethod
    def clean_convert_to_lowercase(_data_obj):
        pass

    @staticmethod
    def set_sentiment(_data_obj, range):
        score = TB(_data_obj.text).sentiment[0]
        _data_obj.valid_sentiment_range = (score >= range[0]) and (score <= range[1])
        