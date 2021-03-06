import pandas as pd
import datetime

locations = [351297, 324152, 354160, 351387, 351683, 324236, 353698, 310126, 324245, 310013, 352197]
weather_url_p1 = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/'
weather_url_p2 = '?res=3hourly&key=a6657747-f1ee-4bc5-be21-270841e3658d'
for loc in locations:
    raw_weather = pd.read_json(weather_url_p1 + str(loc) + weather_url_p2)
    cur_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")
    raw_weather.to_json('frc\\' + cur_time_stamp + '-id-' + str(loc) + '-frc.json')
