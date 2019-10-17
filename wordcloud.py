from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
from nltk.corpus import stopwords
import pickle
from tweet_feed import Feed
from basic_cleaner import BasicCleaner as bc
  
# Read CSV 

file_path = "C:/Users/Joakim/Desktop/test/feed2/191017-15_13_26--191017-15_13_46" # Input file
feed = Feed()
queue_stream = feed.disk_get_tweet_queue(file_path)
l = [x.text for x in queue_stream]
combined_string = ""
for x in l:
    cleaner = bc(x, True)
    text = cleaner.get_text_processed()
    combined_string += f" {text}"

stopwords = set(STOPWORDS) 



  
WC = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(combined_string) 
  
# plot WC                       
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(WC) 
plt.axis("off") 
plt.tight_layout(pad = 0) 


plt.show() 