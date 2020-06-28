import scrapy


class GamerankingsItem(scrapy.Item):
    genre = scrapy.Field()
    game = scrapy.Field()
    totalOverall = scrapy.Field()
    numberPlayers = scrapy.Field()
    numberTournaments = scrapy.Field()
