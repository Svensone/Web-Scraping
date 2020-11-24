import scrapy

class BaliSpider(scrapy.Spider):

    name = 'bali'
    def start_requests(self):
        urls =[
        "https://infocorona.baliprov.go.id/API/pendataan/laporan-harian-01.php",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_items)

    def parse_items(self, response):

        url = response.url
        date = response.css('div#alert alert-info::text').get()
        dailyData = response.xpath('//div[@class=table-responsive text-centered]//text').getall()

        print("url is {}".format(url))
        print('date is {}'.format(date))
        
        # data = CovidData()
        # data['url'] = response.url
        # data['date'] = response.css('div#alert alert-info::text').extract_first()
        # data['dailyData'] = response.xpath('//div[@class=table-responsive text-centered]//text').extract()

# from scrapy.spider import Spider
# from scrapy.http import Request
# from myproject.items import Fixture

# class GoalSpider(Spider):
#     name = "goal"
#     allowed_domains = ["whoscored.com"]
#     start_urls = (
#         'http://www.whoscored.com/',
#         )

#     def parse(self, response):
#         return Request(
#             url="http://www.whoscored.com/Players/3859/Fixtures/Wayne-Rooney",
#             callback=self.parse_fixtures
#         )

#     def parse_fixtures(self,response):
#         sel = response.selector
#         for tr in sel.css("table#player-fixture>tbody>tr"):
#              item = Fixture()
#              item['tournament'] = tr.xpath('td[@class="tournament"]/span/a/text()').extract()
#              item['date'] = tr.xpath('td[@class="date"]/text()').extract()
#              item['team_home'] = tr.xpath('td[@class="team home "]/a/text()').extract()
#              yield item