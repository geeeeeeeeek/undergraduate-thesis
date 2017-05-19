
from pymongo import MongoClient
import os

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']
id_list = [info['id'] for info in shanghai_parks_info.find({}, {'id': 1})]

for number in id_list:
    tf_idf_pos_path = 'assets/shanghai_parks_poi_reviews_pseg/tf_idf/{k}'.format(k=number)
    tf_idf_pos_selections = []
    with open(tf_idf_pos_path, 'r') as fp:
        for i in xrange(10):
            line = fp.readline().strip()
            splitted_items = line.split()
            if len(splitted_items) == 0:
                continue
            else:
                tf_idf_pos_selections.append(splitted_items[0])
    shanghai_parks_reviews.find_one_and_update({'id': number}, {'$set': {
        'keywords': tf_idf_pos_selections
    }})