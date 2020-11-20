import scrapy
import csv

class BaliSpider(scrapy.Spider):

    name = 'bali'

    start_urls = [
        # 'https://pendataan.baliprov.go.id/',
        "https://infocorona.baliprov.go.id/",
        ]

    def parse(self, response):


## Refactor ###
#####################

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