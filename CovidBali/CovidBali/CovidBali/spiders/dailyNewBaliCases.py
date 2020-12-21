import scrapy
from scrapy.item import Item, Field

## unlike pendataan Bali - this one provides new cases on yesterday
## scrapying daily data from Bali Province with API
# created normal in items.py
class BaliItem(Item):
    date = Field()
    data = Field()

class BaliSpider(scrapy.Spider):

    name = 'bali'
    start_urls =[
        "https://infocorona.baliprov.go.id/API/pendataan/laporan-harian-01.php",
        'https://infocorona.baliprov.go.id/API/pendataan/laporan-harian-02.php'
        ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'baliCovid-{page}.html'
        update_date = response.css('div.alert::text')[1].get()

        item = BaliItem()
        item['date'] = update_date[-14:-2]
        item.setdefault('data', [])
        
        for row in response.css('tbody tr'):
            regencyData = row.css('td::text').getall()
            regencyData.append(update_date[-14:-2])
            item['data'].append(regencyData)

        return item
