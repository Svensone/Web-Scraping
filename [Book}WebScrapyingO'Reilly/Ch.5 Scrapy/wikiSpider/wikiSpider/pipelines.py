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

    def process_item(self, article, spider):

        # process 'lastUpdatet' - delete in spider parse_items function
        # dateStr = article['lastUpdated']
        # previously done in parse_items()
        article['lastUpdated'] = article['lastUpdated'].replace("This page was last edited on", '')
        # convert str to python 'datetime' format (strip whitespace before)

        ### comment out next lines since error in processing lastUpdated
        # article['lastUpdated'] = article['lastUpdated'].strip()
        # article['lastUpdated'] = datetime.strptime(article['lastUpdated'], '%d %B %Y, at %H:%M.')
        
        # clean article['text']
        article['text'] = [line for line in article['text'] if line not in whitespace]
        # .join() can be used also on Dict ('key') thus versatiler than concatenate
        article['text'] = ''.join(article['text'])
        return article
