import tweepy
import credentials

class Test_streamer(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        # // AA: 420 is the error code when a rate limit is reached
        if status_code == 420: 
            print("Recieved rate limit warning, stopping stream")
            return False
        else:
            print(f"misc error: {status_code}")



auth = credentials.auth
api = tweepy.API(auth)

SL = Test_streamer()
stream = tweepy.Stream(auth = auth, listener=SL)
stream.sample()