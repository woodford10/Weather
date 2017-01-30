import pymongo
import re


connection = pymongo.MongoClient("mongodb://localhost")
db = connection.sugarkube

rainID = []
rainx = re.compile('snow|storm|flood|cats and dogs|raining|sleet|rainfall|raindrops|sprinkle|spitting|spit|stormy|wet|rain|rainy|pouring|drizzle|shower',re.IGNORECASE)
weathertweets = db.tweets.find({"W2": "Y"})

rain = db.tweets.find({'text': rainx})

for i in rain:
    rainID.append(i['_id'])


print rainID

list3 = []
for i in rainID:
    list3.append(str(i))

print len(list3)

for x in weathertweets:
    id1 = str(x['_id'])

    if id1 in list3:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Rain': 'Y'}})
    else:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Rain': 'N'}})

#####cold
coldID = []
coldx = re.compile('chilly|chill|frosty|frost|wintry|frozen|shivery|snow|ice|sleety|sleet|icy|cold',re.IGNORECASE)
weathertweets = db.tweets.find({"W2": "Y"})

cold = db.tweets.find({'text': coldx})

for i in cold:
    coldID.append(i['_id'])

print coldID

list4 = []
for i in coldID:
    list4.append(str(i))

print len(list4)

for x in weathertweets:
    id1 = str(x['_id'])

    if id1 in list4:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Cold': 'Y'}})
    else:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Cold': 'N'}})

####sun/warm
warmID = []
warmx = re.compile('warm|hot|hotter|warmer|pleasant|boiling|heat|warmish|toasty|summery',re.IGNORECASE)
weathertweets = db.tweets.find({"W2": "Y"})

warm = db.tweets.find({'text': warmx})

for i in warm:
    warmID.append(i['_id'])

print warmID

list5 = []
for i in warmID:
    list5.append(str(i))

print len(list5)

for x in weathertweets:
    id1 = str(x['_id'])

    if id1 in list5:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Warm': 'Y'}})
    else:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Warm': 'N'}})

windyID = []
windyx = re.compile('windy|stormy|gusty|gust|wind|storm|blustery|breeze',re.IGNORECASE)
weathertweets = db.tweets.find({"W2": "Y"})

windy = db.tweets.find({'text': windyx})

for i in windy:
    windyID.append(i['_id'])

print windyID

list6 = []
for i in windyID:
    list6.append(str(i))

print len(list6)

for x in weathertweets:
    id1 = str(x['_id'])

    if id1 in list6:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Windy': 'Y'}})
    else:
        db.tweets.update({'_id': x['_id']}, {'$set': {'Windy': 'N'}})