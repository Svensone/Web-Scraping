# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from datetime import datetime
from items import Article
from string import whitespace

## don't forget to add Pipeline in settings.py
class WikispiderPipeline(object):
    # process_item mandatory (used to process data so parse_items in spider focus on requests)
    def process_item(self, Article, spider):

        ## process 'lastUpdatet' - delete in spider parse_items function
        ## previously done in parse_items()
        Article['lastUpdated'] = Article['lastUpdated'].replace('This page was last edited on', '')
        ### convert str to python 'datetime' format (strip whitespace before)
        ### comment out next lines since error in processing lastUpdated
        Article['lastUpdated'] = Article['lastUpdated'].strip()
        Article['lastUpdated'] = datetime.strptime(Article['lastUpdated'], '%d %B %Y, at %H:%M.')
        
        # clean Article['text']
        Article['text'] = [line for line in Article['text'] if line not in whitespace]
        Article['text'] = ''.join(Article['text'])
        # .join() can be used also on Dict ('key') thus versatiler than concatenate
        return Article
