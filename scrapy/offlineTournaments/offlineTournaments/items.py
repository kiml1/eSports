import scrapy


class OfflinetournamentsItem(scrapy.Item):
    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    totalOnline = scrapy.Field()
    results = scrapy.Field()
    mostGame = scrapy.Field()
    mostGameResults = scrapy.Field()
