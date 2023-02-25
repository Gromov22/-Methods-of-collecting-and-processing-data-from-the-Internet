# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MvideoParsingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    engine = scrapy.Field()
    power = scrapy.Field()
    transmission = scrapy.Field()
    drive = scrapy.Field()
    body = scrapy.Field()
    color = scrapy.Field()
    mileage = scrapy.Field()
    steering_wheel = scrapy.Field()
    generation = scrapy.Field()
    equipment = scrapy.Field()
    _id = scrapy.Field()