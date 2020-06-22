import scrapy


class EarningshistoryItem(scrapy.Item):
    year = scrapy.Field()
    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    totalYear = scrapy.Field()
    totalOverall = scrapy.Field()
