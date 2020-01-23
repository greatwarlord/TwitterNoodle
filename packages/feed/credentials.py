# // AA: Putting credentials here for tidiness
import tweepy

consumer_key = "eHQ2LzLB2BuZ53k4NsXP6Y1py"
consumer_secret = "2CTzpEOuV9bE7IvYQyB1OGqbafVdkoOPiM0vo3nDOHK39r1lmn"

token_key = "933431503773683714-QS96wvzmvNHJgAwHxbjKCoWVmLWy0Zm"
token_secret = "opXFpURvdrlZVW1doZ6fn0uMKGA2vBNM8qK5ynU85UTeR"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token_key, token_secret)