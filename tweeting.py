import weather_info
import tweepy
import random
from random import randrange
import time
import schedule

# Adds an item to the end of the list and removes the first item of the list
def pop_to_end(lst, item):
    lst.append(item)
    del lst[0]


# Represents a twitter bot
class MyTwitterBot:

    # Given the needed keys, constructs the twitter bot and stores the API field
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        # Sets up the API
        authenticator = tweepy.OAuth1UserHandler(api_key, api_key_secret)
        authenticator.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(authenticator, wait_on_rate_limit=True)

        # Keeps track of last 3 replied-to tweets
        self.replied = [0 for x in range(10)]
        mentions = self.api.mentions_timeline(count=10)
        mentions.reverse()
        for mention in mentions:
            pop_to_end(self.replied, mention.id)
    

    # Given text, tweets out the text
    def tweet(self, text):
        self.api.update_status(text)
    

    # Tweets a new weather fact
    def tweet_weather_fact(self):
        weather_tweet = weather_info.get_weather_tweet()
        self.tweet(weather_tweet)
    

    # Retweets a new tweet
    def new_retweet(self):
        # Pre-selected accounts to retweet from
        ids = ["weatherchannel", "NWS", "EmojiWeatherUSA", "NOAA", "accuweather", "wunderground"]

        # Gets the tweets/retweets of a random account from above, then retweets the first tweet it can
        tweets = self.api.user_timeline(screen_name=random.choice(ids), count=20, exclude_replies=True)
        for tweet in tweets:
            if not tweet.retweeted:
                self.api.retweet(tweet.id)
                return
    

    # Updates by either sending a new tweet or retweeting another tweet
    def update(self):
        # 60% chance of new tweet, 40% chance of retweet
        num = randrange(5)
        if num < 3:
            self.tweet_weather_fact()
        else:
            self.new_retweet()
    

    # Checks for mentions and gives a weather forecast to specific replies
    def check_mentions(self):
        mentions = self.api.mentions_timeline(count=3)
        mentions.reverse()

        # Goes through each mention, checking whether to try to reply with a forecast or not
        for mention in mentions:
            if not mention.id in self.replied:
                pop_to_end(self.replied, mention.id)
                tweet_text = mention.text.replace("@fred_weatherman ", "")

                # Attempts to reply with a forecast
                try:
                    # Gets weather tweet, then constructs the main tweet
                    ending = weather_info.get_city_forecast(tweet_text)
                    username = mention.user.name
                    screen_name = mention.user.screen_name
                    tweet_reply = f"@{screen_name} Hi {username}, {ending}"

                    # Sends the reply
                    self.api.update_status(status=tweet_reply, in_reply_to_status_id=mention.id)
                except:
                    # Does not reply to the mention
                    pass


    # Finds new posts to like
    def like_posts(self):
        # Tracks accounts that have already had posts liked from
        already_liked = []

        # Creates an iterable with tweets that have a certain hashtag
        hashtag_choices = ["#weather", "#nature", "#forecast"]
        tweets = tweepy.Cursor(self.api.search_tweets, random.choice(hashtag_choices), result_type="mixed", count=200).items(200)
        i = 0

        # Iterates through the tweets
        for tweet in tweets:
            screen_name = tweet.user.screen_name
            # Ensures that certain conditions are met before trying to like the tweet
            if (screen_name != "fred_weatherman") and (not screen_name in already_liked) and (tweet.lang == "en") and (not tweet.favorited):
                already_liked.append(screen_name)
                # Uses a try-except to ensure the program does not crash while running
                try:
                    self.api.create_favorite(tweet.id)
                    i += 1
                    time.sleep(4)
                except:
                    pass
            # Exits the loop once a certain number of tweets has been reached
            if i >= 5:
                return



# Updates the bot
def updating():
    bot.update()
    print("Just updated the bot.")


# Likes some posts
def update_likes():
    bot.like_posts()
    print("Just liked some posts.")


# Defining the API keys
api_key = "" ## INSERT API KEY HERE
api_key_secret = "" ## INSERT API KEY HERE
access_token = "" ## INSERT API KEY HERE
access_token_secret = "" ## INSERT API KEY HERE

# Creating the bot
bot = MyTwitterBot(api_key, api_key_secret, access_token, access_token_secret)

print("Running version 1.4.4 ......")

# Assigns the task
schedule.every(2).hours.do(updating)
schedule.every(23).minutes.do(update_likes)

# Enters the loop
print("Starting the loop")
while True:
    schedule.run_pending()
    bot.check_mentions()
    time.sleep(30)
