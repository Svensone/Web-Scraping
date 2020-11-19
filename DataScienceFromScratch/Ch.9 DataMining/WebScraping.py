from lxml import html
import csv
import os
import json
import requests
# from exceptions import ValueError
from time import sleep

def AmazonProductParser(url):
    heading={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
        }
    # unlike in book has to be "headers" not "heading"
    page = requests.get(url, headers = heading)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//span[@id="productTitle"]//text()'
            XPATH_DEAL_PRICE = '//span[contains(@id,"priceblock_ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_REAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_STOCK_AVAILABILITY = '//div[@id="availability"]//text()'
            
            PRODUCT_NAME = doc.xpath(XPATH_NAME)
            PRODUCT_DEAL_PRICE = doc.xpath(XPATH_DEAL_PRICE)
            PRODUCT_CATEGORY = doc.xpath(XPATH_CATEGORY)
            PRODUCT_REAL_PRICE = doc.xpath(XPATH_REAL_PRICE)
            PRODUCT_STOCK_AVAILABILITY = doc.xpath(XPATH_STOCK_AVAILABILITY)

            NAME = ''.join(''.join( PRODUCT_NAME).split()) if PRODUCT_NAME else None
            DEAL_PRICE = ''.join(''.join( PRODUCT_DEAL_PRICE).split()).strip() if PRODUCT_DEAL_PRICE else None
            CATEGORY = ''.join([i.strip() for i in PRODUCT_CATEGORY]) if PRODUCT_CATEGORY else None
            REAL_PRICE = ''.join( PRODUCT_REAL_PRICE).strip() if PRODUCT_REAL_PRICE else None
            AVAILABILITY = ''.join( PRODUCT_STOCK_AVAILABILITY).strip() if PRODUCT_STOCK_AVAILABILITY else None
            if not REAL_PRICE:
                REAL_PRICE = DEAL_PRICE
            if page.status_code != 200:
                raise ValueError('captha')
            data = {
                "NAME": NAME,
                'DEAL_PRICE':DEAL_PRICE,
                'CATEGORY':CATEGORY,
                'REAL_PRICE':REAL_PRICE,
                'STOCK_AVAILABILITY':AVAILABILITY,
                'URL':url,
                }
            return data
        except Exception as e:
            print(e)

# Asin is the Sneaker Product Identity Number we will look up
def ReadAsin():
    AsinList = ['B07XTPG1K9', 'B07DPRQMDH', 'B0711R2TNB', 'B07417N22S',
    'B073Y6MPR3', 'B0711R2TNB', 'B000ARG5T8', 'B00D881KE6', 'B07TWMDM6Z',
    'B07FYB1H5J',]

    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print("Processing: " + url)
        extracted_data.append(AmazonProductParser(url))
        sleep(5)
    # path to save file

    path = "DataScienceFromScratch\Ch.9 DataMining"

    f = open(path + "Sneakers.json", "w")
    json.dump(extracted_data, f, indent=4)
    print("Done and finito scraping Sneakers")

if __name__ == "__main__":
    ReadAsin()

