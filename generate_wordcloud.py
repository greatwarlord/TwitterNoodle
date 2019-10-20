from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import pandas as pd 
from tweet_feed import Feed
from basic_cleaner import BasicCleaner
import data_object
  




file_path = "../DataCollection/191020-18_19_45--191020-18_19_47" 



def get_long_tweet_string():
    feed = Feed()
    queue_stream = feed.disk_get_tweet_queue(file_path)
    data_objects = [data_object.get_dataobj_converted(tweet) for tweet in queue_stream]
    #cleaned_data_objects = [BasicCleaner.autocleaner(obj, False) for obj in data_objects]
    for obj in data_objects: BasicCleaner.autocleaner(obj, False)
    long_string = [obj.text for obj in data_objects]
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