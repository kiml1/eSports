import scrapy


class Earningsu18Item(scrapy.Item):
    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    totalU18 = scrapy.Field()
    earliestPrize = scrapy.Field()
    earliestPrizeAge = scrapy.Field()
    totalOverall = scrapy.Field()
