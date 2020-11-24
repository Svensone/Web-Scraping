import scrapy

class Bali2Spider(scrapy.Spider):

    name = 'bali2'

    ## get older dates by changing URL 'tanggal=2020-11-03'
    # try this: https://stackoverflow.com/questions/62687877/scrapy-start-url-using-date-range
    # same ? https://intellipaat.com/community/51555/scrapy-start-url-using-date-range
    
    start_urls = [
        "https://pendataan.baliprov.go.id/map_covid19/search?_token=cxTcYY048Tq8V2BvucUMNEBqvZxZmmMWGPfOqhJ4&level=kabupaten&kabupaten=&tanggal=2020-11-03"
    ]

    def parse(self, response):

        url = response.url.split("/")[-3]
        date = response.css('div.card-header h3::text')[1].get()

        data = response.css('div.col-md-4 ul').getall()
        headers = response.css('div.col-md-4 ul h4::text').getall()
        test = response.xpath('/html/body/div/div/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[2]/ul/li[1]/ul')
        test_data = []
        for item in test.xpath('//li'):
            data1 = item.xpath('text()').extract()
            test_data.append(data1)

        yield {
            'url' : url,
            "date": date,
            "headers": headers,
            'positives_Province' : test_data
            # 'data': data,
        }