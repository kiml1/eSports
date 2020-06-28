from earningsU18.items import Earningsu18Item
from scrapy import Spider, Request
import re


class EarningsU18Spider(Spider):
    name = 'earningsU18_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = [
        'https://www.esportsearnings.com/players/under-eighteen-earnings']

    def parse(self, response):
        players = response.xpath('//tr[@class="format_row highlight"]')

        for player in players:
            country = player.xpath('.//img/@title').extract_first()
            playerID = player.xpath('.//a/text()').extract()[0]
            playerName = player.xpath('.//a/text()').extract()[1]
            totalU18 = float(''.join(re.findall(
                r'\d+|[.]', player.xpath('.//td[@class="format_cell detail_list_prize"]/text()').extract()[0])))
            earliestPrize = player.xpath(
                './/td[@class="format_cell detail_list_prize"]/text()').extract()[1]
            earliestPrizeAge = player.xpath(
                './/td[@class="format_cell detail_list_prize border_right"]/text()').extract_first()
            totalOverall = float(''.join(re.findall(r'\d+|[.]', player.xpath(
                './/td[@class="format_cell detail_list_prize border_left"]/text()').extract_first())))

            item = Earningsu18Item()
            item['country'] = country
            item['playerID'] = playerID
            item['playerName'] = playerName
            item['totalU18'] = totalU18
            item['earliestPrize'] = earliestPrize
            item['earliestPrizeAge'] = earliestPrizeAge
            item['totalOverall'] = totalOverall

            yield item
