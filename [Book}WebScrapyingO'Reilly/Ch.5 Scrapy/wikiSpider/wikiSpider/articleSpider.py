## Ch. 5 Part 3: Creating Items
##############

# from items.py get Article object to store data from scrapying

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import Article



class ArticleSpider(CrawlSpider):

    name = 'articleItems'

    allowed_domains = ['wikipedia.org']

    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']

    # allow url starts with /wiki/ and no colon
    rules = [Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), 
    callback= 'parse_items', follow = True)]


    def parse_items(self, response):

        # add Article Obj. to store data
        article = Article()

        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')

        return article

## run this file with:
## scrapy runspider articleItems.py -o article.csv (or .json/.xml) -t csv