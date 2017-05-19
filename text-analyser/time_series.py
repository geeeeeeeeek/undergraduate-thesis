# -*- coding: utf-8 -*-
from __future__ import division

import logging
import os
import collections
import math

from datetime import datetime

from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
rcParams['figure.figsize'] = 15, 6

client = MongoClient('localhost', 27017)
db = client['poi']
shanghai_parks_info = db['shanghai_parks_info']
shanghai_parks_reviews = db['shanghai_parks_reviews']

class TimeSeriesExtractor:
    def write_csv(self, number):
        review_list = shanghai_parks_reviews.find_one({'id': number})['reviewList']

        time_series_dict = {}

        for review in review_list:
            key = review['addTime'][:10]
            if time_series_dict.has_key(key):
                time_series_dict[key] += 1
            else:
                time_series_dict[key] = 1

        sorted_keys = sorted(time_series_dict)
        with open('assets/time_series/' + str(number) + '.csv', 'w+') as fp:
            fp.write('Date,#Visitors\n')
            for key in sorted_keys:
                fp.write('{key},{value}\n'.format(key=key, value=time_series_dict[key]))
    
    def check_stationarity(self, number):
        dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
        data = pd.read_csv('assets/time_series/' + str(number) + '.csv', parse_dates=['Date'], index_col='Date', date_parser=dateparse)

        ts = data['#Visitors']

        ts_log = np.log(ts)

        ts_log_diff = ts_log - ts_log.shift()

        from statsmodels.tsa.arima_model import ARIMA
        from statsmodels.tsa.stattools import acf, pacf
        
        model = ARIMA(ts_log, order=(2, 1, 2))  
        results_ARIMA = model.fit(disp=-1)  
        # plt.plot(ts_log_diff)
        # plt.plot(results_ARIMA.fittedvalues, color='red')
        # plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
        # plt.show()

        predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
        # print predictions_ARIMA_diff.head()
        predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
        # print predictions_ARIMA_diff_cumsum.head()

        predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
        predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
        # predictions_ARIMA_log.head()

        plt.plot(ts_log)
        plt.plot(predictions_ARIMA_log)
        plt.show()
        return ts

    def test_stationarity(self, timeseries):
        #Determing rolling statistics
        rolmean = pd.rolling_mean(timeseries, window=12)
        rolstd = pd.rolling_std(timeseries, window=12)

        #Plot rolling statistics:
        orig = plt.plot(timeseries, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show()
        
        #Perform Dickey-Fuller test:
        print 'Results of Dickey-Fuller Test:'
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
            dfoutput['Critical Value (%s)'%key] = value
        print dfoutput

num = 1797025
e = TimeSeriesExtractor()
# e.write_csv(num)
ts = e.check_stationarity(num)

