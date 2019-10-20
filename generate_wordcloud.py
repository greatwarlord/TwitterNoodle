from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import pandas as pd 
from tweet_feed import Feed
from basic_cleaner import BasicCleaner
import data_object




file_path = "../DataCollection/191020-20_39_57--191020-20_40_07" 
sentiment_range = [float(-1), float(-0.5)]



def get_long_tweet_string():
    feed = Feed()
    queue_stream = feed.disk_get_tweet_queue(file_path)
    data_objects = [data_object.get_dataobj_converted(tweet) for tweet in queue_stream]
    for obj in data_objects: BasicCleaner.autocleaner(obj,sentiment_range, True)
    long_string = [obj.text*(obj.valid_sentiment_range) for obj in data_objects]
    return " ".join(long_string)



WC = WordCloud(width = 800, height = 800, 
                background_color ='white',  
                min_font_size = 10).generate(get_long_tweet_string()) 
  
# plot WC                       
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(WC) 
plt.axis("off") 
plt.tight_layout(pad = 0) 


plt.show() 