# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    characters = scrapy.Field()
    overview = scrapy.Field()
