from offlineTournaments.items import OfflinetournamentsItem
from scrapy import Spider, Request
import re


class OfflineTournamentsSpider(Spider):
    name = 'offlineTournaments_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = [
        'https://www.esportsearnings.com/players/most-offline-tournament-results']

    def parse(self, response):
        # each page shows the stats from 100 players. Find the href to the top 200, 300, 400 and/or 500.
        topX00 = list(set(response.xpath(
            '//nav[@class="navoptions_box detail_box_nav_big"]/a/@href').extract()))
        # the first top 100 players's url is the url itself without any additional hrefs
        topX00.append(response.url[-40:])
        topX00_urls = [
            f'https://www.esportsearnings.com{href}' for href in topX00]

        # go for each 100 players stats page
        for X00 in topX00_urls:
            yield Request(url=X00, callback=self.parse_100_page)

    def parse_100_page(self, response):
        players = response.xpath('//tr[@class="format_row highlight"]')

        for player in players:
            country = player.xpath('.//img/@title').extract_first()
            playerID = player.xpath('.//a/text()').extract()[0]
            playerName = player.xpath('.//a/text()').extract()[1]
            totalOnline = float(''.join(re.findall(r'\d+|[.]', player.xpath(
                './/td[@class="format_cell detail_list_prize"]/text()').extract_first())))
            results = player.xpath(
                './/td[@class="format_cell detail_list_prize border_right"]/text()').extract_first()
            mostGame = player.xpath(
                './/td[@class="format_cell detail_list_game border_left"]/a/text()').extract_first()
            mostGameResults = player.xpath(
                './/td[@class="format_cell detail_list_prize"]/text()').extract()[1]

            item = OfflinetournamentsItem()
            item['country'] = country
            item['playerID'] = playerID
            item['playerName'] = playerName
            item['totalOnline'] = totalOnline
            item['results'] = results
            item['mostGame'] = mostGame
            item['mostGameResults'] = mostGameResults

            yield item
