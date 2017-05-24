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

logger = logging.getLogger(__name__)

workdays = [(2017, 1, 2), (2017, 1, 22), (2017, 2, 4), (2017, 4, 1), (2016, 2, 6), (2016, 2, 14), (2016, 6, 12), (2016, 9, 18), (2016, 10, 8), (2016, 10, 9), (2015, 1, 4), (2015, 2, 15), (2015, 2, 28), (2015, 10, 10)]
holidays = [(2017, 1, 1), (2017, 1, 2), (2017, 1, 27), (2017, 1, 28), (2017, 1, 29), (2017, 1, 30), (2017, 1, 31), (2017, 2, 1), (2017, 2, 2), (2017, 4, 2), (2017, 4, 3), (2017, 4, 4), (2017, 5, 1),
(2016, 1, 1), (2016, 2, 7), (2016, 2, 8), (2016, 2, 9), (2016, 2, 10), (2016, 2, 11), (2016, 2, 12), (2016, 2, 13), (2016, 2, 7), (2016, 4, 4), (2016, 5, 1), (2016, 5, 2), (2016, 6, 9), (2016, 6, 10), (2016, 6, 11), (2016, 9, 15), (2016, 9, 16), (2016, 9, 17), (2016, 10, 1), (2016, 10, 2), (2016, 10, 3), (2016, 10, 4), (2016, 10, 5), (2016, 10, 6), (2016, 10, 7),
(2015, 1, 1), (2015, 1, 2), (2015, 1, 3), (2015, 2, 18), (2015, 2, 19), (2015, 2, 20), (2015, 2, 21), (2015, 2, 22), (2015, 2, 23), (2015, 2, 24), (2015, 4, 5), (2015, 4, 6), (2015, 5, 1), (2015, 6, 22), (2015, 9, 27), (2015, 10, 1), (2015, 10, 2), (2015, 10, 3), (2015, 10, 4), (2015, 10, 5), (2015, 10, 6), (2015, 10, 7)]

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']

class VisitorGroupPreferenceExtractor:
    def do(self):
        id_list = [info['id'] for info in shanghai_parks_info.find({}, {'id': 1})]

        rate_list = []
        # Iterate over reviews fetched previously
        for number in id_list:
            # Read review body
            review_list = shanghai_parks_reviews.find_one({'id': number})['reviewList']
            workday_review_count = 0
            holiday_review_count = 0

            for review in review_list:
                date = datetime.datetime.strptime(review['addTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                y, m, d = date.year, date.month, date.day
                if y < 2015:
                    continue
                
                is_workday = self.is_workday(y, m, d)
                if is_workday:
                    workday_review_count += 1
                else:
                    holiday_review_count += 1
            
            if holiday_review_count == 0 or workday_review_count == 0:
                continue
            
            rate_list.append(math.log(workday_review_count / 5 / holiday_review_count * 2))
            # self.write_to_mongo(number, workday_review_count, holiday_review_count)

        pp.plot(rate_list, [0] * len(rate_list), 'x')
        pp.xlabel("Visitor Group Preference")
        pp.show()

    def is_workday(self, y, m, d):
        date = datetime.datetime(y, m, d)
        day_of_a_week = date.weekday()

        if (day_of_a_week < 5):
            return (y, m, d) not in holidays
        else:
            return (y, m, d) in workdays
    
    def write_to_mongo(self, id, w, h):
        shanghai_parks_reviews.find_one_and_update({'id': id}, {'$set': {
            'workdayVisits': w,
            'holidayVisits': h,
            'workdayAverageVisits': w / 5,
            'holidayAverageVisits': h / 2,
            'visitorGroupPreferenceIndex': math.log((w / 5) / (h / 2))
        }})

VisitorGroupPreferenceExtractor().do()