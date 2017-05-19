# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient

with open('assets/shanghai_trips_poi_list_with_locations.txt', 'r') as fp:
    content = fp.read()

poi_list = json.loads(content)
print len(poi_list)

categoryName_filter = [u'主题乐园', u'游乐园', u'动物园', u'植物园', u'海洋馆', u'公园']
filtered_list = [
    {
        'branchName': poi['branchName'],
        'categoryId': poi['categoryId'],
        'categoryName': poi['categoryName'],
        'defaultPic': poi['defaultPic'],
        'id': poi['id'],
        'lat': poi['lat'],
        'lng': poi['lng'],
        'matchText': poi['matchText'],
        'name': poi['name'],
        'originalUrlKey': poi['originalUrlKey'],
        'priceText': poi['priceText'],
        'regionName': poi['regionName'],
        'shopType': poi['shopType'],
    }
    for poi in poi_list
    if poi['categoryName'] in categoryName_filter
]

print len(filtered_list)

client = MongoClient('localhost', 27017)
db = client['poi']
collection = db['shanghai_parks_info']
result = collection.insert_many(filtered_list)

print result.inserted_ids