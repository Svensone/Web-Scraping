import scrapy


## scrapying daily data from Bali Province with API

class BaliSpider(scrapy.Spider):

    name = 'bali'
    start_urls =[
        "https://infocorona.baliprov.go.id/API/pendataan/laporan-harian-01.php",
        ]

    def parse(self, response):
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
