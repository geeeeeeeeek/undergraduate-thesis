# -*- coding: utf-8 -*-
from __future__ import division

import logging
import os
import collections
import math
import datetime
from pymongo import MongoClient
import matplotlib.pyplot as pp
import numpy
from snownlp import SnowNLP

logger = logging.getLogger(__name__)

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']

class SentimentsExtractor:
    def do(self):
        id_list = [info['id'] for info in shanghai_parks_info.find({}, {'id': 1})]

        flag = False
        # Iterate over reviews fetched previously
        for number in id_list:
            if number == 2232208:
                flag = True

            if not flag:
                continue

            # Read review body
            review_list = shanghai_parks_reviews.find_one({'id': number})['reviewList']
            workhour_count = 0
            offworkhour_count = 0

            review_sentiments = []
            if len(review_list) == 0:
                continue

            for review in review_list:
                content = review['reviewBody']
                try:
                    s = SnowNLP(content)
                except Exception:
                    continue
                review_sentiments.append(s.sentiments)
            print number, sum(review_sentiments) / len(review_sentiments)

            self.write_to_mongo(number, sum(review_sentiments) / len(review_sentiments))

    def is_workday(self, y, m, d, h):
        date = datetime.datetime(y, m, d)
        if h > 24:
            date += datetime.timedelta(days=1)
        day_of_a_week = date.weekday()

        if (day_of_a_week < 5):
            return (y, m, d) not in holidays
        else:
            return (y, m, d) in workdays
    
    def is_workhour(self, h):
        return 8 < (h % 24) < 18
    
    def write_to_mongo(self, id, sentiments):
        shanghai_parks_reviews.find_one_and_update({'id': id}, {'$set': {
            'sentiments': sentiments
        }})

SentimentsExtractor().do()