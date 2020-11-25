## testing scrapying data from different dates

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from datetime import timedelta, date

class BaliCrawl(CrawlSpider):
    name = 'bali3'

    allowed_domains = []
    
    start_date = date(2020, 11, 1)
    end_date = date(2020, 11, 10) 

    def daterange(start_date, end_date):
        # get the dates wanted
        for n in range((end_date - start_date).days):
            yield start_date + timedelta(n)
    

    start_urls = []
    start_url = "https://pendataan.baliprov.go.id/map_covid19/search?_token=cxTcYY048Tq8V2BvucUMNEBqvZxZmmMWGPfOqhJ4&level=kabupaten&kabupaten=&tanggal="

    # loop over daterange() results and append to url
    for single_date in daterange(start_date, end_date):
        start_urls.append(single_date.strftime(start_url+ "%Y-%m-%d"))
    
    Rule(LinkExtractor(), callback='parse_item', follow=True)

    
    def parse_item(self, response):

        url = response.url
        date = response.url[-9:]

        print(date)
        
        yield {
            'url': url,
            'date': date
        }
