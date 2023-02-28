# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def clean_name(value):
    if ': ' in value[0]:
        for ind, el in enumerate(value[0]):
            if el == ':':
                value = value[0][ind:]
                value = value.replace(': ', '')
                return value
    else:
        return value


def clean_price(value):
    try:
        value = value[0].replace('\xa0', ' ')
    except:
        return value
    return value


class Book24Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(clean_name))
    author = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    discont_price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
