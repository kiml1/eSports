import scrapy


class EsportsItem(scrapy.Item):
    #year = scrapy.Field()
    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    #totalYear = scrapy.Field()
    totalOverall = scrapy.Field()
    game = scrapy.Field()
