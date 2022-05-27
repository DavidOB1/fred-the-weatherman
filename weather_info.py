import requests
import random
from random import randrange
import time


# Defining the API keys
weather_api_key = ""  ## INSERT API KEY HERE
second_api_key = "" ## INSERT API KEY HERE


# A dictionary to convert temperature conditions to emojis
emoji_dict = {
    "Thunderstorm" : "⛈️",
    "Drizzle" : "🌦️",
    "Rain" : "🌧️",
    "Snow" : "❄️",
    "Mist" : "🌫️",
    "Smoke" : "🔥",
    "Haze" : "🌫️",
    "Dust" : "🌫️",
    "Fog" : "🌫️",
    "Sand" : "🌫️",
    "Dust" : "🌫️",
    "Ash" : "🌫️",
    "Squall" : "💨",
    "Tornado" : "🌪️",
    "Clear" : "☀️",
    "Clouds" : "⛅"
}


# Returns the name of the city for the URL
def city_name(city_pair):
    return ",".join(city_pair)


# Returns the name of the city for the tweets
def tweet_city_name(city_pair):
    if city_pair[0] == "New York":
        return "New York City, New York"
    else:
        return ", ".join(city_pair)


# Return the hashtags of the city and its state
def hashtag_city(city_pair):
    if city_pair[0] == "New York":
        return "#NYC #NewYork"
    else:
        city = city_pair[0].replace(" ", "").replace(".", "")
        state = city_pair[1].replace(" ", "")
        return f"#{city} #{state}"


# Returns a string version of the given temperature, with the degree symbol added
def tweet_temp(temperature):
    return f"{str(temperature)}°F"


# Converts Kelvin temperatures to F
def convert_temp(temperature):
    return round((temperature * 1.8) - 459.67)


# Returns a list of pairs of (City, State) for 1000 cities in the US
def get_city_list():
    with open("us_cities.txt") as f:
        cities = [city.split(",") for city in f.read().splitlines()]
        cities = [(city[1], city[2]) for city in cities]
    
    # Removes St. Petersburg Florida since it was giving issues with St. Petersburg Russia
    # And removing DC sicne it causes issues (since it's not in a state)
    # Plus: Removing Toledo due to confusion with Toledo Spain
    del cities[77]
    del cities[66]
    del cities[22]

    # Returns the final list
    return cities


# Returns the weather data of the given city
# Returns just the temperature weather, or the entire weather if given the boolean False
def get_weather_data(city, api_key, main_data=True):
    # Retrieves the weather data
    weather_data_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name(city)}&appid={api_key}"
    weather_data = requests.get(weather_data_url).json()

    # Ensures that the correct city was chosen, updates it if not
    if weather_data["sys"]["country"] != "US":
        weather_data_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name(city)},USA&appid={api_key}"
        weather_data = requests.get(weather_data_url).json()   

    # Returns the weather data dictionary
    if main_data:
        return weather_data["main"]
    else:
        return weather_data


# Given a number, returns a dictionary of weather data of the first n cities
def get_weather_dict(n):
    cities = get_city_list()[:n]
    output = {}
    for i in range(n):
        city = cities[i]
        if i < 60:
            output[city] =  get_weather_data(city, weather_api_key)
        else:
            output[city] =  get_weather_data(city, second_api_key)
    return output


# Returns a tweet about the weather in a random city
def random_city_fact():
    cities = get_city_list()[:150]
    city = random.choice(cities)
    weather_data = get_weather_data(city, weather_api_key)
    
    # Get the opening of the tweet
    opening_type = randrange(7)
    if opening_type == 0:
        opening = f"Just stopped by {tweet_city_name(city)} to visit some friends and family."
    elif opening_type == 1:
        opening = f"I'm on a short road trip right now and decided to take a quick stop in {tweet_city_name(city)}."
    elif opening_type == 2:
        opening = f"I'm headed to an important meeting today and stopped real quick at {tweet_city_name(city)}."
    elif opening_type == 3:
        opening = f"Just had a flat tire, so I guess I'll be in {tweet_city_name(city)} for the next little bit."
    elif opening_type == 4:
        opening = f"Been doing a ton of traveling lately, so I've settled down in {tweet_city_name(city)} for now."
    elif opening_type == 5:
        opening = f"Heard that {tweet_city_name(city)} is a really cool city, so I've finally arrived here."
    else:
        opening = f"Heading home right now and decided to take a quick stop in {tweet_city_name(city)}."
    
    temperature = convert_temp(weather_data["temp"])
    mid_type = randrange(2)

    # Below 30 degrees  
    if temperature < 30:
        if mid_type == 0:
            mid = f"I'm definitely staying inside though, it's literally {tweet_temp(temperature)} outside!!! How can people survive in this? 🥶🥶🥶"
        else:
            mid = f"Won't stay here long though, I stepped outside and was hit hard by the {tweet_temp(temperature)} weather! It's sooooooo cold 🥶🥶🥶🥶"
    # 30 to 45 degrees
    elif temperature < 45:
        if mid_type == 0:
            mid = f"It's kinda cold here though, with the temperature sitting just at {tweet_temp(temperature)}. Make sure to bring a coat outside!"
        else:
            mid = f"Feelin kinda cold though, {tweet_temp(temperature)} outside rn. Make sure to bring a coat here!"
    # 45 to 60 degrees
    elif temperature < 60:
        if mid_type == 0:
            mid = f"Temperature here is just a little chilly, sitting at {tweet_temp(temperature)}."
        else:
            mid = f"Right now it's {tweet_temp(temperature)} here. Not too bad, but I wish it was a bit warmer out."
    # 60 to 78 degrees
    elif temperature < 78:
        mid = f"Really glad I stopped by here, it's {tweet_temp(temperature)} outside right now, feels really nice!"
    # 78 to 90 degrees
    elif temperature < 90:
        if mid_type == 0:
            mid = f"Right now it's {tweet_temp(temperature)} outside. Really wish it was a bit cooler tbh."
        else:
            mid = f"Starting to sweat a bit in this {tweet_temp(temperature)} weather, but at least it's nice outside here."
    # Above 90 degrees
    else:
        if mid_type == 0:
            mid = f"I don't plan on staying here for long though, it's literally {tweet_temp(temperature)} outside! How do people survive in this??? 🥵🥵🥵🥵"
        else:
            mid = f"I'm definitely staying inside for most of today, the temperature here is {tweet_temp(temperature)}!!! Soooo hot today 🥵🥵🥵"

    tweet = opening + " " + mid + "\n" + hashtag_city(city)
    return tweet


# Gets a tweet about a very warm or very cold city right now
def extreme_temp_fact():
    weather_dict = {k: v["temp"] for k, v in get_weather_dict(100).items()}

    # Determines whether to get the highest or coldest temperature, then gets the city list
    high_temp = randrange(2) == 0
    top = sorted(weather_dict.items(), key=lambda x: x[1], reverse=high_temp)[:3]
    random.shuffle(top)
    
    # Constructs the tweet
    if high_temp:
        mid = "warmest"
    else:
        mid = "coldest"

    tweet = f"Here are some of the {mid} places in the US to be right now:\n"
    hashtags = []

    for pair in top:
        name = tweet_city_name(pair[0])
        temperature = convert_temp(pair[1])
        temp_reading = tweet_temp(temperature)
        tweet += f"{name}: {temp_reading}\n"
        hashtag = "#" + pair[0][0].replace(" ", "")
        hashtags.append(hashtag)
    
    tweet += " ".join(hashtags)

    # Retrun the final tweet
    return tweet

# Gets a tweet about a place that feels warmer than the temperature actually reports it to be
def difference_temp_fact():
    # Gets the data for the difference in temperature versus the actual temperature, and creates a sorted list
    weather_dict = get_weather_dict(100)
    diff_dict = {k: v["feels_like"] - v["temp"] for k, v in weather_dict.items()}
    top_list = sorted(diff_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Picks a city from one of the top 3
    top = random.choice(top_list)[0]

    # Extracts the data
    weather_data = weather_dict[top]
    rec_temp = convert_temp(weather_data["temp"])
    feels_like = convert_temp(weather_data["feels_like"])

    # Determines if the temperature difference is large enough
    # If not, returns a new randomized weather tweet after waiting for a minute to reset the API keys
    if abs(feels_like - rec_temp) < 3:
        time.sleep(60)
        return get_weather_tweet()

    # Constructs the parts of the tweet
    open_type = randrange(3)
    if open_type == 0:
        opening = f"Be careful of the weather if you're in {tweet_city_name(top)} right now."
    elif open_type == 1:
        opening = f"Don't be fooled by the forecast for {tweet_city_name(top)}."
    else:
        opening = f"Make sure to double check the weather forecast in {tweet_city_name(top)} right now."
    
    mid = f"Even though it says the temperature is {tweet_temp(rec_temp)}, it actually feels closer to {tweet_temp(feels_like)}!"

    # Puts together the tweet and returns it
    tweet = opening + " " + mid + "\n" + hashtag_city(top)
    return tweet


# Returns a tweet that gives a brief forecast of major cities
def quick_forecast_tweet():
    # Gets the top cities and prepares the tweet
    top_cities = get_city_list()[:6]
    random.shuffle(top_cities)
    
    tweet = "5 Second Forecast:\n"

    # Gets the weather data for each city and constructs the tweet
    for city in top_cities:
        weather_data = get_weather_data(city, weather_api_key, False)
        weather_condition = weather_data["weather"][0]["main"]
        emoji = emoji_dict[weather_condition]
        temperature = convert_temp(weather_data["main"]["temp"])

        # Updates the emoji if it is night time
        if (emoji == "🌦️") or (emoji == "⛅") or (emoji == "☀️"):
            time_now = weather_data["dt"]
            if (time_now < weather_data["sys"]["sunrise"]) or (time_now > weather_data["sys"]["sunset"]):
                emoji = "🌖"

        tweet += f"{tweet_city_name(city)}: {tweet_temp(temperature)} {emoji}\n"
    
    # Returns the tweet
    return tweet + "#WeatherForecast"


# Gets a tweet about a city with a big change in temperature
def temp_change_tweet():
    # Gets the data for the change in temperature, and creates a sorted list
    weather_dict = get_weather_dict(115)
    diff_dict = {k: v["temp_max"] - v["temp_min"] for k, v in weather_dict.items()}
    top_list = sorted(diff_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    random.shuffle(top_list)

    # Constructs the tweet
    tweet = "Looks like the temperature will vary a lot in these cities:\n"

    for pair in top_list:
        city = pair[0]
        weather_data = weather_dict[city]
        hi_temp = convert_temp(weather_data["temp_max"])
        lo_temp = convert_temp(weather_data["temp_min"])
        tweet += f"{tweet_city_name(city)}: High of {tweet_temp(hi_temp)}, Low of {tweet_temp(lo_temp)}\n"

    return tweet[:-1]    


# Gets a random weather fact to tweet about
def get_weather_tweet():
    random_num = randrange(4)
    # Picks a random type of tweet to return
    if random_num == 0:
        return random_city_fact()
    elif random_num == 1:
        return extreme_temp_fact()
    elif random_num == 2:
        return difference_temp_fact()
    else:
        return quick_forecast_tweet()
    # For now I will not be using the temp_change_tweet() tweets
    

# Given a city name, returns a weather forecast for that city (partial tweet)
def get_city_forecast(city_name):
    # Collects the data
    weather_data = get_weather_data((city_name, "USA"), weather_api_key, False)

    # Picks apart the data
    name = weather_data["name"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = str(weather_data["main"]["humidity"]) + "%"
    weather_condition = weather_data["weather"][0]["main"]
    emoji_condition = emoji_dict[weather_condition]

    # Updates the emoji if it is night time
    if (emoji_condition == "🌦️") or (emoji_condition == "⛅") or (emoji_condition == "☀️"):
        time_now = weather_data["dt"]
        if (time_now < weather_data["sys"]["sunrise"]) or (time_now > weather_data["sys"]["sunset"]):
            emoji_condition = "🌖"
    
    # Constructs the tweet
    tweet = f"here's the weather in {name} right now:\n"
    tweet += f"Current Temp: {tweet_temp(convert_temp(temperature))}\n"
    tweet += f"Feels Like: {tweet_temp(convert_temp(feels_like))}\n"
    tweet += f"Humidity: {humidity}\n"
    tweet += f"Condition: {emoji_condition}\n"
    tweet += "#WeatherForecast"

    # Returns the tweet
    return tweet
