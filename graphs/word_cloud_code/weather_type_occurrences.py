
# coding: utf-8

# In[1]:

import pymongo
import pandas as pd


# In[14]:

import datetime as dt


# In[2]:

weather_pd = pd.read_pickle(r'..\weather_data.pki')
weather_pd.head()


# In[3]:

weather_obs = weather_pd[['city','date_time_period','w_observed']]


# In[4]:

weather_obs = weather_obs.drop_duplicates(subset=['city', 'date_time_period'])


# In[5]:

weather_dates = pd.DataFrame(columns=['dates'])


# In[6]:

list(weather_obs.ix[weather_obs['w_observed'].apply(lambda x: 1 in x if type(x)==list else 1 == x), 'date_time_period'].values)


# In[7]:

weather_dates = pd.DataFrame(columns=['dates'])
weather_types = {
    'Cloudy':[2,3,7,8],
    'Clear Night': [0],
    'Fog': [5, 6],
    'Rain': [9,10,11,12,13,14,15]
}
for w_type in weather_types:
    for i in weather_types[w_type]:
            if w_type not in weather_dates.index:
                weather_dates.loc[w_type, 'dates'] = list(weather_obs.ix[weather_obs['w_observed'].apply(lambda x: i in x if type(x)==list else i == x), 'date_time_period'].values)
            else:
                weather_dates.loc[w_type, 'dates'].extend(list(weather_obs.ix[weather_obs['w_observed'].apply(lambda x: i in x if type(x)==list else i == x), 'date_time_period'].values))


# In[8]:

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.sugarkube
tweets_db = db.tweets


# In[15]:

# weather_obs.ix[weather_obs['w_observed'].apply(lambda x: i in x if type(x)==list else i == x), 'date_time_period'].to_datetime


# In[16]:

# [dt.datetime.utcfromtimestamp(a.tolist()/1e9) for a in weather_dates.loc['Rain', 'dates']]


# In[17]:

# tweets_db.find({'date_time_period':{'$in':[dt.datetime.utcfromtimestamp(a.tolist()/1e9) for a in weather_dates.loc['Rain', 'dates']]}})


# In[33]:

from bson.json_util import dumps


# In[47]:

popular_words = tweets_db.aggregate(pipeline=[
        {
    "$match": {'date_time_period':{'$in':[dt.datetime.utcfromtimestamp(a.tolist()/1e9) for a in weather_dates.loc['Cloudy', 'dates']]}}
}, 
    {
    "$project": {
        'text': '$text'
        , "_id": 0
    }
}])


# In[48]:

with open('cloudy_tweets.json','w') as outfile:
    outfile.write(dumps(popular_words))


# In[42]:




# In[ ]:



