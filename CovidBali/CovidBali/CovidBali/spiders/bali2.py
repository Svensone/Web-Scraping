import scrapy

class Bali2Spider(scrapy.Spider):

    name = 'bali2'

    ## get older dates by changing URL 'tanggal=2020-11-03'
    # try this: https://stackoverflow.com/questions/62687877/scrapy-start-url-using-date-range
    # same ? https://intellipaat.com/community/51555/scrapy-start-url-using-date-range

    # next steps
    # - get data clean from start_url
    # - get past dates data (see link above)
    # = clean code (implement Items and Pipeline)
    
    start_urls = [
        "https://pendataan.baliprov.go.id/map_covid19/search?_token=cxTcYY048Tq8V2BvucUMNEBqvZxZmmMWGPfOqhJ4&level=kabupaten&kabupaten=&tanggal=2020-11-03"
    ]

    def parse(self, response):

        url_name = response.url.split("/")[-3]
        date = response.url[-9:]
        date_info = response.css('div.card-header h3::text')[1].get()

        # get case numbers
        data = response.css('div.col-md-4 ul').getall()
        provinces = response.css('div.col-md-4 ul h4::text').getall()
        
        ulist = response.xpath('//ul[@style="list-style: none;"]/li/ul')
        
        ## option 1 both produce repeated data entries
        # start fresh 
        # 1) get all ul with pos.cases - check len
        # 2) iterate over and create list
        pos_cases = []
        for item in ulist.xpath('//li/ul'):
            per_province = []
            for sel in item.xpath('//li'):
                number = sel.xpath('text()').extract()
                per_province.append(number)
            pos_cases.append(per_province)
        ## option 2
        # pos_cases = ulist.xpath('//li/ul/li/text()').extract()
        
        # extract the other cases
        other_cases = ulist.xpath('//li/p/text()').extract()

        ## combine data - use pipeline for data munging

        yield {
            'url' : url_name,
            "date": date,
            "headers": provinces,
            'positives_Province' : pos_cases,
            # 'other_cases': other_cases,
        }