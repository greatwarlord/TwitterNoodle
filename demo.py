#repo
from packages.dataset_tools.generate_dataset import Generate_Dataset as gd #1
from packages.cleaning.basic_cleaner import BasicCleaner as bc             #4
from packages.dataset_tools.scale_dataset import DatasetScalingHelper      #2
from packages.feed.tweet_feed import Feed                                  #3
from process_tools import ProcessSimilarity
#from packages.graphical.generate_wordcloud import write_csv
from packages.cleaning.custom_stopwords import main


#mods
import csv
import seaborn as sb



generator = gd(
    _runtime_total = 20, 
    _runtime_between_slices = 20, 
    _runtime_forever = False, 
    _out_directory = 'C:/Users\Erlend-PC/Documents/Coding/Noodle/TwitterNoodle-master/packages/', 
    _track_keywords = main())


generator.run_collector()


# // MERGE

# scale = DatasetScalingHelper(_verbosity = True)
# scale.set_dir_input('C:\\Users\\Joakim\\Desktop\\TwitterNoodle-master\\packages\\zIN')
# scale.set_dir_output('C:\\Users\\Joakim\\Desktop\\TwitterNoodle-master\\packages\\zOUT')
# scale.merge_datasets_by_directory()



# fp = 'C:\\Users\\Joakim\\Desktop\\TwitterNoodle-master\\200116-15_06_06--200116-15_06_11.csv'
# def lds(_verbosity: bool = True) -> None:
#     ''' Example of loading datasets and cleaning it too + printout.

#     '''
#     feed = Feed()
#     obj_list = feed.disk_get_tweet_queue(fp)
#     #print(len(obj_list))
#     for obj in obj_list:
#         bc.autocleaner(obj, _sentiment_range = [float(-1),float(0)], _verbosity = False)
#         print(obj.text)

# #csvf = write_csv('200116-16_18_53--200116-16_18_58.csv')

# lds()
# #csvf



# lds()


# sim = ProcessSimilarity()
# #sim.get_model_info()
# sim.load_model()
# # query = "window"
# # txt = [
# #     "car",
# #     "bus",
# #     "cat",
# #     "dog",
# #     "economy",
# #     "money"
# #     ]
# # for item in txt:
# #     score = sim.get_score(query, item , 2)
# #     print(f"{query} + {item} = {score}")

# result = sim.get_similarity_net(query = ['window'], current_recursion = 0, max_recursion = 2)
# for i in result:
#     print(i)