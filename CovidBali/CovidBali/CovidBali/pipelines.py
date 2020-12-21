# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class CovidbaliPipeline:
    def process_item(self, item, spider):
        return item

# pipeline to export data
# https://stackoverflow.com/questions/43023693/scrapy-how-to-output-items-in-a-specific-json-format/43698923

class JsonPipeline(object):

    def open_spider(self, spider):
        self.file = open('daily.jl', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(
            dict(item),
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        ) + ",\n"

        self.file.write(line)

        return item