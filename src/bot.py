import aiohttp
import asyncio
import discord
import logging
import math
import random
import re
import tweepy
from googletrans import Translator
from tweepy import OAuthHandler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "NjEzMTI0NjA4MzU0Mjg3Nzg3.XVsXCg.jTPbdAWLqd64y6SjMaxsYQTrsC0"

quotes = ["'Weddings are basically funerals with cake.' - Rick", 
    "'So what if he's the devil, Rick? At least the devil has a job. At least he's active in the community.' - Summer", 
    "'What, so everyone is supposed to sleep every single night now. You realize that nighttime makes up half of all time?' - Rick", 
    "'Nobody exists on purpose. Nobody belongs anywhere. Everybody's gonna die. Come watch TV.' - Morty", 
    "'You ever hear about Wall Street, Morty? Y-you know what those guys do in their fancy board rooms? They take their balls and they dip them in cocaine and wipe them all over each other' -Rick", 
    "'I hate to break it to you, but what people call \"love\" is just a chemical reaction that compels animals to breed. It hits hard, Morty, then it slowly fades, leaving you stranded in a failing marriage. I did it. Your parents are going to do it. Break the cycle, Morty. Rise above. Focus on science.' - Rick",
    "'I miss my family. I miss my laptop. I masturbated to an extra curvy piece of driftwood the other day!' - Morty",
    "'I'm sorry, Summer. Your opinion means very little to me.' - Rick",
    "'Listen, I'm not the nicest guy in the universe because I'm the smartest. And being nice is something stupid people do to hedge their bets. Now, I haven’t been exactly subtle about how little I trust marriage. I couldn’t make it work, and I could turn a black hole into a sun, so at a certain point, you’ve got to ask yourself what are the odds this is legit and not just some big lie we’re all telling ourselves because we’re afraid to die alone? Because, you know, that’s exactly how we all die … alone. But … but … Here’s the thing. Birdperson is my best friend, and if he loves Tammy, well, then I love Tammy, too. [Cheers and applause] To friendship, to love, and to my greatest adventure yet … opening myself up to others.' - Rick",
    "'What up, my glip-glops?' - Rick",
    "'Yeah, I'd like to order one large phone with extra phones, please. Cell phones. No-no-no-no, rotary! And pay phone on half.' - a couch person",
    "'You gotta do it for Gandpa, Morty. You gotta put these seeds inside your butt.' - Rick",
    "'Don't move. Gonorrhea can't see us if we don't move... Wait! I was wrong! I was thinking of a T-Rex.' - Rick",
    "'Traditionally, science fairs are a father-son thing. Well, scientifically, traditions are an idiot thing.' - Rick",
    "'If I sounded a little defensive, it's because Pirates of the Pancreas was my baby. I got a lot of push-back hwne i pitched it, Morty. I guess I'm still a little defensive' - Rick",
    "'Oh Summer, [laughing] first race war, huh?' - Morty",
    "'I’ll tell you how I feel about school, Jerry: It’s a waste of time. Bunch of people runnin’ around bumpin’ into each other, got a guy up front says “2 + 2,” and the people in the back say, “4.” Then the bell rings and they give you a carton of milk and a piece of paper that says you can go take a dump or somethin’. I mean, it’s not a place for smart people, Jerry. I know that’s not a popular opinion, but that’s my two cents on the issue.' - Rick",
    "'Mm, there is no God, Summer. You got to rip the band-aid off now. You'll thank me later.' - Rick",
    "'Listen Morty, I hate to break it to you, but what people calls “love” is just a chemical reaction that compels animals to breed. It hits hard, Morty, then it slowly fades, leaving you stranded in a failing marriage. I did it. Your parents are gonna do it. Break the cycle, Morty. Rise above. Focus on science.' - Rick",
    "'Listen to me, Morty. I know that new situations can be intimidating. You lookin’ around and it’s all scary and different, but y’know … meeting them head-on, charging into ‘em like a bull — that’s how we grow as people.' - Rick",
    "'Having a family doesn’t mean that you stop being an individual. You know the best thing you can do for the people that depend on you? Be honest with them, even if it means setting them free.' - Mr. Meeseeks",
    "'Well then get your shit together, get it all together and put it in a backpack, all your shit, so it’s together. And if you gotta take it somewhere, take it somewhere, you know. Take it to the shit store and sell it, or put it in the shit museum. I don’t care what you do, you just gotta get it together. Get your shit together.' - Morty"
]

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

	def get_tweets(self, query, count):
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

# create discord client
client = discord.Client()
# create sentiment analyzer object
analyzer = SentimentIntensityAnalyzer()
translator = Translator()

def sentiment_analyzer_scores(text):
    trans = translator.translate(text).text
    score = analyzer.polarity_scores(trans)
    lb = score['compound']
    print(score)
    if lb >= 0.05:
        return 'positive'
    elif (lb > -0.05) and (lb <0.05):
        return 'neutral'
    else:
        return 'negative'

def random_quote():
    return quotes[random.randint(1,len(quotes)) % len(quotes)]

def poll(query, count = 25):
    api = TwitterClient()
    tweets = api.get_tweets(query, count) 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] >= 0.05]
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] <= -0.05]
    a = ("Positive tweets percentage: {} %\n".format(100*len(ptweets)/len(tweets)))
    b = ("Neutral tweets percentage: {} %\n".format(100*((len(tweets) - len(ntweets) - len(ptweets))/len(tweets))))
    c = ("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    return a + b + c
    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('quote'):
        print('quote is firing')
        await message.channel.send(random_quote())
    elif message.content.startswith('poll'):
        print('checking twitter')
        try:
            results = poll(message.content.split(' ', 2)[2], message.content.split(' ', 2)[1])
        except IndexError:
            try:
                results = poll(message.content.split(' ', 2)[1])
            except IndexError as e:
                print('Error: ' + str(e))
                results = 'Try adding a query after the poll command.'
        await message.channel.send(results)
    else:
        sentiment = sentiment_analyzer_scores(message.content)
        print('sentiment: ' + str(sentiment))
        await message.channel.send('The sentiment of your text is ' + str(sentiment))

client.run(TOKEN)
