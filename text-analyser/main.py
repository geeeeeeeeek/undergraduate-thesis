import logging
import ConfigParser
logger = logging.getLogger(__name__)

from keyword_extraction import KeywordExtractor

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

    if not is_enabled:
        continue
    
    KeywordExtractor(section).do()
