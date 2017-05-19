import logging
import ConfigParser
import json

from poi_list import POIListCrawler
from poi_reviews import POIReviewsCrawler
from poi_location import POILocationCrawler
from poi_reviews_full import POIFullReviewsCrawler

# Setup logging options
logging.basicConfig(
    level='INFO',
    filename='history.log',
    format='%(asctime)s[%(levelname)s][%(filename)s.%(funcName)s]%(message)s')

# Read parameters from conf
config = ConfigParser.RawConfigParser()
config.read('default.cfg')

for section in config.sections():
    is_enabled = config.getboolean(section, 'enabled')
    items = config.items(section)
    handler = config.get(section, 'handler')

    if not is_enabled:
        continue
    
    if handler == 'poi_list':
        items = {
            'start': config.getint(section, 'start'),
            'maximum': config.getint(section, 'maximum'),
            'categoryid': config.getint(section, 'categoryid'),
            'keyword': config.get(section, 'keyword'),
            'output_name': section
        }
        POIListCrawler(items).do()

    elif handler == 'poi_reviews':
        with open('assets/{n}.txt'.format(n=config.get(section, 'list'))) as fp:
            poi_list = fp.read()
        items = {
            'list': json.loads(poi_list),
            'output_name': section
        }
        POIReviewsCrawler(items).do()
    
    elif handler == 'poi_reviews_full':
        items = {
            'output_name': section
        }
        POIFullReviewsCrawler(items).do()
    
    elif handler == 'poi_location':
        list_name = config.get(section, 'list')
        with open('assets/{n}.txt'.format(n=list_name)) as fp:
            poi_list = fp.read()
        items = {
            'list': json.loads(poi_list),
            'list_name': list_name
        }
        POILocationCrawler(items).do()