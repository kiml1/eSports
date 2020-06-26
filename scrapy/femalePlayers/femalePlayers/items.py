import scrapy


class FemaleplayersItem(scrapy.Item):
    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    totalOverall = scrapy.Field()
    game = scrapy.Field()
    gameEarningRatio = scrapy.Field()
