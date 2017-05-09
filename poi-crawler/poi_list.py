import logging
import requests
import json
import time

logger = logging.getLogger(__name__)

class POIListCrawler:
    def __init__(self, items):
        self.start = items['start']
        self.maximum = items['maximum']
        self.categoryid = items['categoryid']
        self.keyword = items['keyword']
        self.output_name = items['output_name']

        self.poi_list = []
        
        self.base_url = 'http://mapi.dianping.com/searchshop.json?start={s}&locatecityid=1&cityid=1&categoryid={c}&keyword={k}'
    
    def do(self):
        while self.start < self.maximum:
            self.get_list()
            time.sleep(0.1)
        self.output_file(self.poi_list)
        time.sleep(30)
        

    def get_list(self):
        url = self.base_url.format(s=self.start, k=self.keyword, c=self.categoryid)
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3091.0 Mobile Safari/537.36'}
        logger.info('URL={u}'.format(u=url))
        try:
            r = requests.get(url, headers=headers)
        except Exception as e:
            logger.error('Error={e}'.format(e=r.context))
        
        poi_list = json.loads(r.content)['list']
        self.poi_list += poi_list

        entry_number = len(poi_list)
        self.start += entry_number
        logger.info('Success. {n} entries fetched.'.format(n=entry_number))

        if entry_number == 0:
            self.start = self.maximum

    def output_file(self, content):
        with open('assets/{n}.txt'.format(n=self.output_name), 'w') as fp:
            fp.write(json.dumps(content,ensure_ascii=False).encode('utf8'))