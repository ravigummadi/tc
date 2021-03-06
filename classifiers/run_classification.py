import sys, os
import pymongo

sys.path.append('..')
from lib import mongodb
from classify_tweets import *

DB_NAME = 'tweets'

if __name__ == '__main__':
    classifiers = []
    for active_classifier in active_classifiers:
        c = globals()[active_classifier]()
        classifiers.append(c)


    db =  mongodb.connect(DB_NAME)
    for r in db[DB_NAME].find(spec={'topics': {'$exists': False } },fields={'text': True, 'user': True}): # for all unclassified tweets
        print r
        topics = {}
        for c in classifiers:
            (topic, score) = c.classify(r['text'])
            topics[topic] = score
        
        print topics
        db[DB_NAME].update({'_id': r['_id']}, {'$set': {'topics': topics }})