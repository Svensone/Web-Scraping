## Ch. 5 Part 2: Spidering with Rules
##############

# extending CrawlSpider class obj. / adding Rule(LinkExtractor) / .xpath('//div[@id="..."]//text).extract() /

## different in new Scrapy Version - no '.contrib'
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticleSpider(CrawlSpider):

    name = 'articles'

    allowed_domains = ['wikipedia.org']

    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']

    # allow all Urls with regex '.*'
    rules = [Rule(LinkExtractor(allow=r'.*'), 
    callback= 'parse_items', follow = True)]


    def parse_items(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        text = response.xpath('//div[@id="mw-content-text"]//text').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()

        print('URL is: {}'.format(url))
        print('title is: {} '.format(title))
        print('text is: {}'.format(text))
        print('Last updated: {}'.format(lastUpdated))
