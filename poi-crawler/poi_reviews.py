import logging
import requests
import json
import time
import os
logger = logging.getLogger(__name__)

class POIReviewsCrawler:
    def __init__(self, items):
        self.list = items['list']

        self.dir_path = 'assets/{n}'.format(n=items['output_name'])
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def do(self):
        counter = 0
        for item in self.list:
            self.get_reviews(item)
            counter += 1
            logger.info('{n} reviews fetched.'.format(n=counter))
            time.sleep(0.1)
        time.sleep(30)

    def get_reviews(self, item):
        url = 'http://m.dianping.com/index/api/module'
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3091.0 Mobile Safari/537.36'}
        payload = {
            'pageEnName':'shopreviewlist',
            'moduleInfoList[0][moduleName]':'reviewlist',
            'moduleInfoList[0][query][shopId]':item['id'],
            'moduleInfoList[0][query][page]':1
        }
        logger.info('URL={u}. ItemId={i}'.format(u=url, i=item['id']))
        try:
            r = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            logger.error('Error={e}'.format(e=r.context))
        
        review_list = json.loads(r.content)['data']['moduleInfoList'][0]['moduleData']['data']['reviewList']

        full_review = ''
        for review in review_list:
            full_review += review['reviewBody'] + '\n===\n'
        logger.info('Success. {n} reviews fetched.'.format(n=len(review_list)))
        
        self.output_file(item['id'], full_review)
        
    def output_file(self, id, content):
        with open('{s}/{n}.txt'.format(s=self.dir_path, n=id), 'w+') as fp:
            fp.write(content.encode('utf8'))