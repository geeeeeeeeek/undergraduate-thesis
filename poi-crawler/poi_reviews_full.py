import logging
import requests
import json
import time
import os
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class POIFullReviewsCrawler:
    def __init__(self, items):
        self.dir_path = 'assets/{n}'.format(n=items['output_name'])
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def do(self):
        client = MongoClient('localhost', 27017)
        db = client['poi']
        shanghai_parks_info = db['shanghai_parks_info']
        shanghai_parks_reviews = db['shanghai_parks_reviews']

        self.list = shanghai_parks_info.find({}, {'id': 1})
        counter = 0
        total = 0
        for item in self.list:
            review_list = []
            if os.path.exists(self.dir_path + '/{m}.txt'.format(m=item['id'])):
                counter += 1
                continue
            
            for i in xrange(1, 51):
                page_review_list = self.get_reviews(item, i)
                if len(page_review_list) == 0:
                    break
                else:
                    review_list += page_review_list
            shanghai_parks_reviews.insert_one({
                'id': item['id'],
                'reviewList': review_list
            })
            reviews_number = len(review_list)
            total += reviews_number
            counter += 1
            logger.info('[{m}] Id: {i}, {n} reviews fetched. Total: {k}.'.format(m=counter, i=item['id'], n=reviews_number, k=total))
            # time.sleep(0.1)
        time.sleep(30)

    def get_reviews(self, item, page):
        url = 'http://m.dianping.com/index/api/module'
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3091.0 Mobile Safari/537.36'}
        payload = {
            'pageEnName':'shopreviewlist',
            'moduleInfoList[0][moduleName]':'reviewlist',
            'moduleInfoList[0][query][shopId]':item['id'],
            'moduleInfoList[0][query][page]':page
        }
        logger.info('URL={u}. ItemId={i}'.format(u=url, i=item['id']))
        try:
            r = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            logger.error('Error={e}'.format(e=r.context))
        
        review_list = json.loads(r.content)['data']['moduleInfoList'][0]['moduleData']['data']['reviewList']
        review_number = len(review_list)
        logger.info('Success. {n} reviews on page {p}.'.format(n=review_number, p=page))
        return review_list
        
    def output_file(self, id, content):
        with open('{s}/{n}.txt'.format(s=self.dir_path, n=id), 'w+') as fp:
            fp.write(json.dumps(content,ensure_ascii=False).encode('utf8'))