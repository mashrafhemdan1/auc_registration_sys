# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CatalogcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    dept_code = scrapy.Field()
    course_num = scrapy.Field()
    course_name = scrapy.Field()
    descrip = scrapy.Field()
    credit = scrapy.Field()
    when_offered = scrapy.Field()
    Crosslisted = scrapy.Field()
    Prerequisites = scrapy.Field()
    notes = scrapy.Field()
    pass

class deptItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass