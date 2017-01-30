import datetime as dt
import ijson
import pymongo
import sys


def str_to_num(num):
    try:
        return float(num)
    except ValueError:
        return num

connection = pymongo.MongoClient("mongodb://localhost")

db = connection.sugarkube
weather_db = db.weather
# weather_db.drop()

locations = [3772, 3134, 3784, 3781]
temp_date = dt.datetime(2016, 12, 9, 10)

while temp_date < dt.datetime.now():
    for loc_id in locations:
        try:
            with open("obs\\"+temp_date.strftime('%Y-%m-%d-%H')+"-id-"+str(loc_id)+"-obs.json") as tweet_file:
                parser = ijson.items(tweet_file, 'SiteRep.DV')
                for obj in parser:
                    weather = []
                    if obj['Location']['i'] == '3134':
                        city = 'glasgow'
                    else:
                        city = 'london'
                    for day_obs in obj['Location']['Period']:
                        if type(day_obs) == dict:
                            for obs in day_obs['Rep']:
                                if type(obs) == dict:
                                    # converts the number of minutes to the hour period previous
                                    temp_hours = ((int(obs['$']) - 1) / 180) * 3
                                    dict_time_key = dt.datetime.strptime(day_obs['value'], '%Y-%m-%dZ') + dt.timedelta(
                                        hours=temp_hours)
                                    weather.append({
                                        'weather': {old_key: str_to_num(obs[old_key]) for old_key in obs.keys() if old_key != '$'}
                                        , 'w_type': 'obs'
                                        , 'date_time_period': dict_time_key
                                        , 'time': obs['$']
                                        , 'city': city
                                        , 'town': obj['Location']['name'].lower()
                                    })
            for obs in weather:
                query = weather_db.find({
                    "time": obs['time'],
                    "w_type": obs['w_type'],
                    'date_time_period': obs['date_time_period'],
                    'town': obs['town']
                })
                if query.count() == 0:
                    weather_db.insert_one(obs)
        except IOError:
            print sys.exc_info()
            print "obs\\"+temp_date.strftime('%Y-%m-%d-%H')+"-id-"+str(loc_id)+"-obs.json"
    temp_date += dt.timedelta(hours=1)

