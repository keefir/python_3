# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    query = scrapy.Field()
    name = scrapy.Field()
    categories = scrapy.Field()
    score = scrapy.Field()
    review_number = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
