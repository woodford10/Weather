import pandas as pd
import datetime

locations = [3772, 3134]
weather_url_p1 = 'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/'
weather_url_p2 = '?res=hourly&key=a6657747-f1ee-4bc5-be21-270841e3658d'
for loc in locations:
    raw_weather = pd.read_json(weather_url_p1 + str(loc) + weather_url_p2)
    cur_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")
    raw_weather.to_json('obs\\' + cur_time_stamp + '-id-' + str(loc) + '-obs.json')

