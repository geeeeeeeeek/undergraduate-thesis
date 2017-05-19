# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']

result = shanghai_parks_info.find({}, {'id': 1})

for item in result:
    with open('assets/shanghai_trips_poi_reviews/{id}.txt'.format(id=item['id']), 'r') as fp:
        content = fp.read()
    reviews_object = {
        'id': item['id']
        'reviewList': json.loads(content)
    }
    shanghai_parks_reviews.insert_one(reviews_object)