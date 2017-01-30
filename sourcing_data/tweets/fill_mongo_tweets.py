import ijson
import pymongo
import datetime as dt
import math


connection = pymongo.MongoClient("mongodb://localhost")

db = connection.sugarkube
tweets = db.tweets

tweets.drop()
temp_date = dt.datetime(2016, 12, 7, 19)

while temp_date < dt.datetime.now():
    time_string = temp_date.strftime('%Y-%m-%d-%H')
    try:
        with open("tweets\\"+time_string+"-tweets.json") as tweet_file:
            parser = ijson.items(tweet_file, 'item')
            for obj in parser:
                try:
                    for i in [0, 1]:
                        obj['coordinates']['coordinates'][i] = float(obj['coordinates']['coordinates'][i])
                except TypeError:
                    pass
                obj['city'] = 'london'
                obj['created_at'] = dt.datetime.strptime(obj['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                obj['date_time_period'] = dt.datetime(obj['created_at'].date().year,
                                                      obj['created_at'].date().month,
                                                      obj['created_at'].date().day,
                                                      int(math.floor(obj['created_at'].time().hour/3)*3))
                tweets.insert_one(obj)
    except IOError:
        pass #error handling so good
    except ijson.common.JSONError:
        print temp_date
    finally:
        temp_date += dt.timedelta(hours=1) #good stuff keep it up
