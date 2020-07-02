import scrapy


class OnlinetournamentsItem(scrapy.Item):

    country = scrapy.Field()
    playerID = scrapy.Field()
    playerName = scrapy.Field()
    totalOnline = scrapy.Field()
    results = scrapy.Field()
    mostGame = scrapy.Field()
    mostGameResults = scrapy.Field()
