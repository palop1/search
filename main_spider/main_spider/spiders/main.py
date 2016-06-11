from __future__ import absolute_import
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from main_spider.items import WebsiteItem

class MainSpider(Spider):

    name = "main"
    #allowed_domains = ["localhost"]
    allowed_domains = ["thebeijinger.com"]  
    #base_url = "http://localhost:8000"
    base_url = "thebeijinger.com"
    pages = []
    crawled = []
    
    start_urls = (
        "http://thebeijinger.com/",
        #'http://localhost:8000/blog/',
    )
    
    rules = (
        Rule(LinkExtractor(allow=(), 
                           restrict_xpaths=('//a[@class="button next"]',)),
                           callback="parse", follow=True),
    )
    
    def parse(self, response):
        if response.url not in self.crawled:
            self.crawled.append(response.url)
            s = Selector(response)
            item = WebsiteItem()    
            item["url"] = [response.url]
            item["header"] = s.xpath("//meta[@name='description']/@content").extract()
            item["body"] = s.xpath("body").extract()
            self.pages.append(item)        

            for url in s.xpath("//a/@href").extract():
                url = self.base_url + str(url)
                if url not in self.crawled:
                    print "New page: " + url
                    try:
                        yield Request(url=url, callback=self.parse)
                    except ValueError:
                        yield Request(url=('http://' + url), callback=self.parse)
            yield item
