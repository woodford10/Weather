import datetime as dt
import pymongo
import re

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.sugarkube
alltweets = db.tweets.find()

weather_tweets_raw_ID = []
weather_tweets_not_ID = []

regx = re.compile("(\s|^)(cold|colder|froze|flood|floods|flooding|fog|freeze|snow|snowing|air|blizzard|blustery|climate|snowy|freezing|condensation|\
dew|draft|chilly|chilling|chill|frost|frosty|ice|iced|icy|cool|cooler|wind|windy|storm|stormy|gust|breeze|breezy|sun|sunny|clear|\
warm|warmer|wet|wetter|rain|rainy|pouring|drizzle|sleet|hail|hailstorm|shower|showers|foggy|lightening|temperature|\
mist|misty|muggy|cloud|clouds|cloudy|thunder|thunderstorms|weather|#weather)\s", re.IGNORECASE)

for x in alltweets:
    tag = (x['text'])
    id1 = str(x['_id'])
    tag1 = re.sub('\\n', '', tag)
    tag2 = re.sub('@\S+', '', tag1)
    db.tweets.update({'_id': x['_id']}, {'$set': {'text': tag2}})

negative_regx = re.compile("(GMT|mm|hPa|mph|kmh|mb|mh|pokemon|barometer)\b", re.IGNORECASE)

weather_tweets_raw = db.tweets.find({'text': regx})
weather_tweets_not = db.tweets.find({'$or': [{'text': regx}, {'text': negative_regx}]})

for i in weather_tweets_raw:
    weather_tweets_raw_ID.append(i['_id'])

for i in weather_tweets_not:
    weather_tweets_not_ID.append(i['_id'])

wtr_ID = []
for i in weather_tweets_raw_ID:
    wtr_ID.append(str(i))

wtn_ID = []
for i in weather_tweets_not_ID:
    wtr_ID.append(str(i))

for tweet in alltweets:
    id1 = str(tweet['_id'])
    if str(id1) in wtr_ID and not str(id1) in wtn_ID:
        db.tweets.update({'_id': tweet['_id']}, {'$set': {'W1': 'Y'}})
    else:
        db.tweets.update({'_id': tweet['_id']}, {'$set': {'W1': 'N'}})
