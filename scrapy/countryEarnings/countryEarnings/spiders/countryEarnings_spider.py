from countryEarnings.items import CountryearningsItem
from scrapy import Spider, Request
import re


class CountryEarnings(Spider):
    name = 'countryEarnings_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = ['https://www.esportsearnings.com/countries']

    def parse(self, response):
        countries = response.xpath('//tr[@class="format_row highlight"]')

        for c in countries:
            country = c.xpath('.//img/@alt').extract_first()
            totalOverall = float(''.join(re.findall(
                r'\d+|[.]', c.xpath('.//td[@class="format_cell detail_list_prize"]/text()').extract_first())))
            numberPlayers = float(''.join(re.findall(
                r'\d+', c.xpath('.//td[@class="format_cell detail_list_prize"]/text()').extract()[1])))

            item = CountryearningsItem()
            item['country'] = country
            item['totalOverall'] = totalOverall
            item['numberPlayers'] = numberPlayers

            yield item
