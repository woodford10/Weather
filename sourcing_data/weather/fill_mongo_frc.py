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

locations = [351297, 324152, 354160, 351387, 351683, 324236, 353698, 310126, 324245, 310013, 352197]
temp_date = dt.datetime(2016, 12, 2, 17)

while temp_date < dt.datetime.now():
    for loc_id in locations:
        try:
            with open("frc\\"+temp_date.strftime('%Y-%m-%d-%H')+"-id-"+str(loc_id)+"-frc.json") as tweet_file:
                parser = ijson.items(tweet_file, 'SiteRep.DV')
                for obj in parser:
                    weather = []
                    if 'Location' in obj.keys():
                        for day_frc in obj['Location']['Period']:
                            if obj['Location']['i'] in ['352197']:
                                city = 'glasgow'
                            elif obj['Location']['i'] in ['310013', '353698', '324236', '324245', '310126']:
                                city = 'manchester'
                            else:
                                city = 'london'
                            for frc in day_frc['Rep']:
                                temp_hours = int(frc['$'])/60
                                dict_time_key = dt.datetime.strptime(day_frc['value'], '%Y-%m-%dZ') + dt.timedelta(hours=temp_hours)
                                str_dict_time_key = dict_time_key.strftime('%Y-%m-%d-%H')
                                frc_period = dict_time_key - dt.datetime.strptime(obj["dataDate"], '%Y-%m-%dT%H:%M:%Sz')
                                weather.append({
                                    'weather': {
                                        old_key: str_to_num(frc[old_key]) for old_key in frc.keys() if old_key != '$'}
                                    , 'w_type': 'frc'
                                    , 'date_time_period': dict_time_key
                                    , 'forecast_on': dt.datetime.strptime(obj["dataDate"], '%Y-%m-%dT%H:%M:%Sz')
                                    , 'forecast_period': frc_period.total_seconds()/3600
                                    , 'city': city
                                    , 'town': obj['Location']['name'].lower()
                                    })
            for frc in weather:
                weather_db.insert_one(frc)
        except IOError:
            pass
    temp_date += dt.timedelta(hours=3)
