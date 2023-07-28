# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IosItem(scrapy.Item):
    name = scrapy.Field()
    provider = scrapy.Field()
    link = scrapy.Field()
    linktype = scrapy.Field()
    tracktype = scrapy.Field()
    notlinkedtype = scrapy.Field()
    rate = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    age = scrapy.Field()
    inpurchases = scrapy.Field()
