# Sentiment Analysis using the Twitter API
import re 
import tweepy 
from tweepy import OAuthHandler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

class TwitterClient(object):
	def __init__(self):
		consumer_key = 'Jc3H9uwEOuJ8xfGZvmI1DzitB'
		consumer_secret = 'siSOYCxXPnO31PdPVeefjlPA86g6JVVli4UkKKnujCMRzBvGde'
		access_token = '964329956376567809-Lo9h6A3nougib6POTyx2qku0lLtpzPz'
		access_token_secret = 'dK64mI0c2Y4NXkc9jI4f6XpqUzxnzEYg1PWzkwDwDakhT'

		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def sentiment_analyzer_scores(self, text):
		analyzer = SentimentIntensityAnalyzer()
		translator = Translator()
		trans = translator.translate(text).text
		score = analyzer.polarity_scores(trans)
		lb = score['compound']
		return lb

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweets(self, query, count = 25):
		tweets = [] 

		try:
			fetched_tweets = self.api.search(q = query, count = count) 

			for tweet in fetched_tweets:
				parsed_tweet = {} 
				parsed_tweet['text'] = tweet.text
				parsed_tweet['sentiment'] = self.sentiment_analyzer_scores(self.clean_tweet(tweet.text))

				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			return tweets 

		except tweepy.TweepError as e:
			print("Error : " + str(e)) 

def main():
	query = input('What should I query? ')
	count = input('How many tweets should I search? ')
	api = TwitterClient()
	tweets = api.get_tweets(query, count) 

	ptweets = [tweet for tweet in tweets if tweet['sentiment'] >= 0.05]
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] <= -0.05]

	print("\nPositive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	print("Neutral tweets percentage: {} %".format(100*((len(tweets) - len(ntweets) - len(ptweets))/len(tweets))))
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

if __name__ == "__main__":
	main() 
