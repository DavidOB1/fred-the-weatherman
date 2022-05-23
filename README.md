# Who is Fred?

Fred is a Twitter bot who tweets cool things about the weather and retweets from other weather accounts.
You can find Fred's twitter here: https://twitter.com/fred_weatherman

The profile picture for the Twitter account is an AI generated face.
You can generate your own AI profile picture at: https://this-person-does-not-exist.com/

# About the Code

This code uses OpenWeatherMap's API to collect data about the weather in US cities in order to make tweets.
Some tweets pick a city at random and make a tweet, while others look at the top 100-120 cities and compare
the weather among them. 

The cities chosen for this were the list of top 1000 cities in the US, sorted by population. Credits to Miserlou for the
data that I used for us-cities.txt, the file can be found here: https://gist.github.com/Miserlou/11500b2345d3fe850c92

In the actual build I have running, I have defined the api keys used for the OpenWeatherMap API and the Twitter API.
If you wish to successfully run this code yourself, you will need to get API keys for both of those.

The code is currently being executed from Heroku (assuming it is still running at the time of you reading this).
You can learn more about Heroku and their hosting services at: https://www.heroku.com/
