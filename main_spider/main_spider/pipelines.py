# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class MainSpiderPipeline(object):

    def process_item(self, item, spider):
        for key in item:
            soup = BeautifulSoup(item[key][0])
            text = soup.getText()
            key = key.encode('ascii','ignore')
            item[key] = text.encode('ascii','ignore').replace("\n", " ")

        json = item.to_JSON()
        es.index(index='page', doc_type='website', id=item["url"], body=json)           
        return item
