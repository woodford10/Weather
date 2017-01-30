from twython import TwythonStreamer
import datetime as dt
import json


CONSUMER_KEY = '######################'
CONSUMER_SECRET = '########################################'
ACCESS_TOKEN = '#################################'
ACCESS_TOKEN_SECRET = '#####################################'


class MyStreamer(TwythonStreamer):
    tweets = []

    def on_success(self, data):
        if data['lang'] == 'en':
            output = {}
            output['text'] = data['text']
            output['coordinates'] = data['coordinates']
            output['created_at'] = data['created_at']
            MyStreamer.tweets.append(output)
            if len(MyStreamer.tweets) > 100 and dt.datetime.now().strftime("%M") == '00':
                try:
                    cur_time_stamp = dt.datetime.now().strftime("%Y-%m-%d-%H")
                    filename = 'tweets\\' + cur_time_stamp + '-tweets.json'
                    f = open(filename, 'a')
                    f.write(json.dumps(MyStreamer.tweets))
                    MyStreamer.tweets[:] = []
                finally:
                    f.close()

    def on_error(self, status_code, data):
        self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream.statuses.filter(locations='-0.500418, 51.338952, 0.199263, 51.665630') # coordinates for London



