# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['domain'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['domain'])
            logging.info('%s discovered', item['domain'])
            return item

    def open_spider(self, spider):
        if hasattr(spider, 'ids_seen'):
            self.ids_seen = spider.ids_seen

    def close_spider(self, spider):
        pass
