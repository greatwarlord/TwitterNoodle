import matplotlib.pyplot as plt 
import pandas as pd 
import csv
from wordcloud import WordCloud 

from packages.feed.tweet_feed import Feed
from packages.cleaning.basic_cleaner import BasicCleaner
from packages.cleaning import data_object



#file_path = "../pickle_saved_data"
file_path = "./datasplit/out/191120-21_34_19--191120-21_35_18" 
sentiment_range = [float(-1), float(1)]

def get_long_tweet_objects():
    feed = Feed()
    queue_stream = feed.disk_get_tweet_queue(file_path)
    data_objects = [data_object.get_dataobj_converted(tweet) for tweet in queue_stream]
    for obj in data_objects: BasicCleaner.autocleaner(obj,sentiment_range, False)
    return data_objects

def get_long_tweet_string():
    long_string = [obj.text*(obj.valid_sentiment_range) for obj in get_long_tweet_objects()]
    return " ".join(long_string)

def generate_wordcloud():
    WC = WordCloud(width = 800, height = 800, 
                    background_color ='white',  
                    min_font_size = 10).generate(get_long_tweet_string()) 
    
    # plot WC                       
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(WC) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show() 

def write_csv(_filename):
    with open(_filename, 'w', newline='') as csvfile:
        obj_writer = csv.writer(csvfile, delimiter=',',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)

        obj_list = get_long_tweet_objects()
        obj_writer.writerow(["name"] + ["txt"] + ["coord"] + ["places"] + ["hashtags"] + ["alphatags"] + ["sentiment"])
        for obj in obj_list:
            try:
                obj_writer.writerow([obj.name] + 
                                    [obj.text] + 
                                    [obj.coordinates] +
                                    [obj.place] + 
                                    [obj.hashtags] +
                                    [obj.alphatags] + 
                                    [obj.valid_sentiment_range])
            except:
                pass


#generate_wordcloud()