
    # next steps
    # - get positive Cases
    # - combine data -> in "oldBaliCases"
    # - add the dailyNewCases
    # = clean code (implement Items and Pipeline)
    
import scrapy
from scrapy.item import Item

class TestData(Item):
    data = scrapy.Field()
    provinces = scrapy.Field()
    positives = scrapy.Field()
    dateData = scrapy.Field()

class Bali2Spider(scrapy.Spider):
    name = 'bali2'

    start_urls = [
        "https://pendataan.baliprov.go.id/map_covid19/search?_token=cxTcYY048Tq8V2BvucUMNEBqvZxZmmMWGPfOqhJ4&level=kabupaten&kabupaten=&tanggal=2020-11-03"
    ]

    def parse(self, response):

        item = TestData()
        # dateCases = str(response.url[-9:])
        # item['dateData'] = dateCases
        
        ## Positiv cases

        table = response.xpath('/html/body/div/div/div/div/div[2]/div/div/div[2]/div/div[1]/ul')
        cases = []
        for ul in table.xpath('//ul'):
            cases = ul.xpath('//li/p/text()').extract()
            cases.append(cases)
        
        item['data'] = cases

        return item