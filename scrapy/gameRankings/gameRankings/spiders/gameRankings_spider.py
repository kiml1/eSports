from gameRankings.items import GamerankingsItem
from scrapy import Spider, Request
import re


class GameRakingsSpider(Spider):
    name = 'gameRankings_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = ['https://www.esportsearnings.com/games/browse-by-genre']

    def parse(self, response):
        genres = response.xpath(
            '//span[@class="games_main_genre_title"]/text()').extract()
        allgames = response.xpath('//div[@class="games_main_genre_body"]')

        for i in range(0, len(genres)):
            genre = genres[i]
            genreGames = allgames[i].xpath(
                './/div[@class="games_main_game_box"]')

            for games in genreGames:
                try:
                    game = games.xpath('.//a/text()').extract_first()
                    totalOverall = float(''.join(re.findall(
                        r'\d+|[.]', games.xpath('.//div[@class="games_main_game_stats"]/text()').extract()[0])))
                    numberPlayers = int(''.join(re.findall(r'\d+', games.xpath(
                        './/div[@class="games_main_game_stats"]/text()').extract()[1])))
                    numberTournaments = int(''.join(re.findall(r'\d+', games.xpath(
                        './/div[@class="games_main_game_stats"]/text()').extract()[2])))
                except:
                    continue

                item = GamerankingsItem()
                item['genre'] = genre
                item['game'] = game
                item['totalOverall'] = totalOverall
                item['numberPlayers'] = numberPlayers
                item['numberTournaments'] = numberTournaments

                yield item
