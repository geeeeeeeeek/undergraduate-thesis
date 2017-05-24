# -*- coding: utf-8 -*-
from __future__ import division

import logging
import os
import collections
import math
import numpy as np

from pymongo import MongoClient
import matplotlib.pylab as plt
import numpy

logger = logging.getLogger(__name__)

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']

class Temp:
    def do(self):
        sentimenets_list = []
        stars_list = []
        result = shanghai_parks_reviews.find({})
        for info in result:
            if len(info['reviewList']) == 0:
                continue
            sentimenets_list.append(info['sentiments'])
            stars_temp = []
            for review in info['reviewList']:
                if 'star' in review:
                    stars_temp.append(review['star']/10)
            stars_list.append(np.average(stars_temp))
        sentiment_avg = np.average(sentimenets_list)
        stars_avg = np.average(stars_list)
        cov_sum = 0
        sx_sum = 0
        sy_sum = 0
        sxy = np.cov(sentimenets_list, stars_list)[0][1]
        sx=np.cov(sentimenets_list, sentimenets_list)[0][1]
        sy=np.cov(stars_list, stars_list)[0][1]
        cor=np.corrcoef(sentimenets_list, stars_list)
        print sxy,sx,sy, cor[0][1]
        plt.scatter(sentimenets_list, stars_list)
        plt.xlabel(u"Sentiments from Reviews")
        plt.ylabel(u"User Ratings")
        plt.show()
Temp().do()