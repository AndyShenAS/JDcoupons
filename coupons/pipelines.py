# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CouponsPipeline(object):
    def process_item(self, item, spider):
        item['good']
        return item

import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('data\\items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if type(line) == str:
            line = line.encode('utf-8')
        self.file.write(line)
        return item