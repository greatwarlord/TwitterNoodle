
import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords

# Downloads nltk stopwords
nltk.download('stopwords')


import_file = "playground/asdf.txt"
l = []


def file_to_list(_in, _list):
    with open(_in, "r") as f:
        content = f.readline()
        while content:
            w = content.strip()
            _list.append(w)
            content = f.readline()


def main():
    file_to_list(import_file, l)
    stop_words = get_stop_words('english')
    nltk_stop_words = set(stopwords.words('english'))
    l.extend(stop_words)
    l.extend(nltk_stop_words)
    return l

