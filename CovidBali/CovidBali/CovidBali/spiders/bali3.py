## testing scrapying data from different dates

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from datetime import timedelta, date

class BaliCrawl(CrawlSpider):
    name = 'bali3'

    allowed_domains = [
        "pendataan.baliprov.go.id"
    ]
    
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
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='example__example']/a"), callback='parse_item', follow=True),)
    
    def parse_item(self, response):
        page = response.url.split("/")[-2]
        filename = f'baliCovid-{page}.html'

        # step 3:
        data = []
        for row in response.css('tbody tr'):
            data.append(row.css('td::text').getall())
            
        update_date = response.css('div.alert::text')[1].get()

        yield {
            'data': data,
            'update_date': update_date,
            }
