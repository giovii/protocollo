# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LolItem(scrapy.Item):
    # define the fields for your item here like:
    champ = scrapy.Field()
    team = scrapy.Field()
    every15 = scrapy.Field()
    fatti= scrapy.Field()
    subiti= scrapy.Field()
    idee = scrapy.Field()

    over = scrapy.Field()
    prova = scrapy.Field()
    date = scrapy.Field()
    home= scrapy.Field()
    score= scrapy.Field()
    away= scrapy.Field()


    pass
