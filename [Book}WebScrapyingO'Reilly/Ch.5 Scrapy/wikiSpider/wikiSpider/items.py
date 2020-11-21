# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

## Ch. 5 Part 3: Creating Items
##############

# new Article object extend the scrapy.Item class
# with scrapy.Field()

import scrapy


class Article(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    lastUpdated = scrapy.Field()

    pass
