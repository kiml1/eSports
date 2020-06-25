import scrapy


class CountryearningsItem(scrapy.Item):
    country = scrapy.Field()
    totalOverall = scrapy.Field()
    numberPlayers = scrapy.Field()
