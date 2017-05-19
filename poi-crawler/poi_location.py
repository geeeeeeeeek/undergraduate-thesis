import logging
import requests
import json
import time
import os
import re

logger = logging.getLogger(__name__)

class POILocationCrawler:
    def __init__(self, items):
        self.list = items['list']
        self.list_name = items['list_name']

    def do(self):
        counter = 0
        for item in self.list:
            lat, lng = self.get_location(item)
            item['lat'] = lat
            item['lng'] = lng
            counter += 1
            logger.info('[{s}] {n} location fetched.'.format(s=self.list_name, n=counter))
            time.sleep(0.1)
        self.output_file(json.dumps(self.list, ensure_ascii=False).encode('utf8'))
        time.sleep(30)

    def get_location(self, item):
        url = 'https://m.dianping.com/shop/{i}/map'.format(i=item['id'])
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3091.0 Mobile Safari/537.36'}
        logger.info('[{s}] URL={u}. ItemId={i}'.format(s=self.list_name, u=url, i=item['id']))
        try:
            r = requests.get(url, headers=headers)
            lat = re.search('lat:\'(.*)\',', r.content).group(1)
            lng = re.search('lng:\'(.*)\',', r.content).group(1)
        except Exception as e:
            logger.error('Error={e}'.format(e=r.context))
            return 0, 0


        logger.info('[{s}] id={i}, lat={a}, lng={b}'.format(s=self.list_name, i=item['id'], a=lat, b=lng))
        return lat, lng
        
    def output_file(self, content):
        with open('assets/{s}_with_locations.txt'.format(s=self.list_name, n=id), 'w+') as fp:
            fp.write(content)