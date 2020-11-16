import scrapy

class BaliSpider(scrapy.Spider):

    name = 'bali'

    start_urls = ['https://pendataan.baliprov.go.id/']

    def parse(self, response):
        yield {
            'number': response.xpath('/html/body/div/div/div/div/div[1]/div[2]/div/div[2]/h1/text()').extract(),
        }
