# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GrustnogramApiParsingItem(scrapy.Item):
    id = scrapy.Field()
    nickname = scrapy.Field()
    name = scrapy.Field()
    avatar = scrapy.Field()
    tag = scrapy.Field()
    _id = scrapy.Field()