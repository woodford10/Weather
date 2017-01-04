import pickle
import nltk
import pymongo


connection = pymongo.MongoClient("mongodb://localhost")
db = connection.sugarkube
alltweets = db.tweets.find({"W1": "Y"})

with open('./Pickles/tweetspickle', 'r') as p1:
    tweets11 = pickle.load(p1)

with open('./Pickles/tweetsplit1', 'r') as p2:
    tweetsfeatures = pickle.load(p2)

with open('./Pickles/classifypick', 'r') as p3:
    classifier = pickle.load(p3)


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in tweetsfeatures:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.apply_features(extract_features, tweets11)

for x in alltweets:
    text = (x['text'])
    if classifier.classify(extract_features(text.split())) == 'y':
        db.tweets.update({'_id': x['_id']}, {'$set': {'W2': 'Y'}})
    else:
        db.tweets.update({'_id': x['_id']}, {'$set': {'W2': 'N'}})
