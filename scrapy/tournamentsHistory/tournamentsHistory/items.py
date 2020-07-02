import scrapy


class TournamentshistoryItem(scrapy.Item):
    year = scrapy.Field()
    totalPrize = scrapy.Field()
    totalTournaments = scrapy.Field()
    totalActivePlayers = scrapy.Field()
    meanTournamentPrizePool = scrapy.Field()
    meanEarningsPlayers = scrapy.Field()
    medianTournamentPrizePool = scrapy.Field()
    medianEarningsPlayers = scrapy.Field()
