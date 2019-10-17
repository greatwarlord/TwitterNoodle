from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import pandas as pd 
from tweet_feed import Feed
from basic_cleaner import BasicCleaner
  

file_path = "../DataCollection/191013-20_25_33--191013-20_26_34" 

def get_text():
    # // AA: Load and clean pickled tweets
    feed = Feed()
    queue_stream = feed.disk_get_tweet_queue(file_path)
    combined_string = ""
    for tweet in queue_stream:
        cleaner = BasicCleaner(tweet.text, True)
        text = cleaner.get_text_processed()
        combined_string += f" {text}"
    return combined_string

def get_text_2():
    # // AA: Load and clean pickled tweets
    feed = Feed()
    queue_stream = feed.disk_get_tweet_queue(file_path)
    tweet_list = [tweet.text for tweet in queue_stream]
    # // AA: return a long string of tweet texts
    return " ".join(tweet_list)



  
WC = WordCloud(width = 800, height = 800, 
                background_color ='white',  
                min_font_size = 10).generate(get_text_2()) 
  
# plot WC                       
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(WC) 
plt.axis("off") 
plt.tight_layout(pad = 0) 


plt.show() 