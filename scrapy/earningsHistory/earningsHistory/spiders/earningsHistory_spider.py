from earningsHistory.items import EarningshistoryItem
from scrapy import Spider, Request
import re


class EsportsSpider(Spider):
    name = 'earningsHistory_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = ['https://www.esportsearnings.com/history']

    def parse(self, response):
        # here I get the href for each year
        years = range(1998, 2021)
        year_urls = [
            f'https://www.esportsearnings.com/history/{year}/top_players' for year in years]

        # go for each year page
        for url in year_urls:
            yield Request(url=url, callback=self.parse_year_page)

    def parse_year_page(self, response):
        # each page shows the stats from 100 players. Find the href to the top 200, 300, 400 and/or 500.
        topX00 = list(set(response.xpath(
            '//div[@class="navoptions_box detail_box_nav_big"]/a/@href').extract()))
        # the first top 100 players's url is the url itself without any additional hrefs
        topX00.append(response.url[-25:])
        topX00_urls = [
            f'https://www.esportsearnings.com{href}' for href in topX00]

        # go for each 100 players stats page
        for X00 in topX00_urls:
            yield Request(url=X00, callback=self.parse_100_page)

    def parse_100_page(self, response):
        year = response.xpath(
            '//h1[@class="detail_box_title"]/text()').extract_first()[-4:]

        players = response.xpath('//tr[@class="format_row highlight"]')

        for player in players:
            country = player.xpath('.//img/@title').extract_first()
            playerID = player.xpath('.//a/text()').extract()[0]
            playerName = player.xpath('.//a/text()').extract()[1]
            totalYear = float(''.join(re.findall(r'\d+|[.]', player.xpath(
                './/td[@class="format_cell detail_list_prize border_right"]/text()').extract_first())))
            totalOverall = float(''.join(re.findall(r'\d+|[.]', player.xpath(
                './/td[@class="format_cell detail_list_prize border_left"]/text()').extract_first())))

            item = EarningshistoryItem()
            item['year'] = year
            item['country'] = country
            item['playerID'] = playerID
            item['playerName'] = playerName
            item['totalYear'] = totalYear
            item['totalOverall'] = totalOverall

            yield item
