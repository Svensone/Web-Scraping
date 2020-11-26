import scrapy
from scrapy.item import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from datetime import timedelta, date


# created normal in items.py
class BaliItem(Item):
    title = Field()
    dateCases = Field()
    provinces = Field()


class MultiDateSpider(scrapy.Spider):
    name = 'bali4'

    allowed_domains = ["pendataan.baliprov.go.id"]

    ## get all URL for the start and end
    start_urls = []
    start_date = date(2020, 11, 1)
    end_date = date(2020, 11, 10) 
    start_url = "https://pendataan.baliprov.go.id/map_covid19/search?_token=cxTcYY048Tq8V2BvucUMNEBqvZxZmmMWGPfOqhJ4&level=kabupaten&kabupaten=&tanggal="
    def daterange(start_date, end_date):
        # get the dates wanted
        for n in range((end_date - start_date).days):
            yield start_date + timedelta(n)
    # loop over daterange() results and append to url
    for date1 in daterange(start_date, end_date):
        start_urls.append(date1.strftime(start_url+ "%Y-%m-%d"))
    
    rules = [Rule(LinkExtractor(allow=r".*"), callback='parse', follow=True)]

    def parse(self, response):
        item = BaliItem()
        item['title'] = response.xpath('/html/body/div/div/div/div/section/div/div/div/h3/text()').extract()
        item['dateCases'] = response.xpath('//h3[@class="section-title"]/text()').extract()[0].split(' ')[-4]

        ## crunch the data!!!
        table = response.xpath('/html/body/div/div/div/div/div[2]/div/div/div[2]/div/div[1]/ul')
        item['provinces'] = table.xpath('//h4/text()').extract()

        return item