from earningsByCountry.items import EarningsbycountryItem
from scrapy import Spider, Request
import re


class EarningsCountrySpider(Spider):
    name = 'earningsCountry_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = ['https://www.esportsearnings.com/countries']

    def parse(self, response):
        # here I get the href for each country to be added to the link
        country_href = response.xpath(
            '//td[@class="format_cell detail_list_player"]/a/@href').extract()[1::2]
        country_urls = [
            f'https://www.esportsearnings.com{href}' for href in country_href]

        # go for each country page
        for url in country_urls:
            yield Request(url=url, callback=self.parse_country_page)

    def parse_country_page(self, response):
        # each page shows the stats from 100 players and some countries have more than 100. Find the href to the top 200, 300, 400 and/or 500.
        topX00 = list(dict.fromkeys(response.xpath(
            '//nav[@class="navoptions_box detail_box_nav_big"]//@href').extract()))
        # the first top 100 players's url is the url itself without any additional hrefs
        topX00.append(response.url[-13:])
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
            totalOverall = float(''.join(re.findall(r'\d+|[.]', player.xpath(
                './/td[@class="format_cell detail_list_prize border_right"]/text()').extract_first())))
            game = player.xpath('.//a/text()').extract()[2]

            item = EarningsbycountryItem()
            item['country'] = country
            item['playerID'] = playerID
            item['playerName'] = playerName
            item['totalOverall'] = totalOverall
            item['game'] = game

            yield item
