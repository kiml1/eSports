from tournamentsHistory.items import TournamentshistoryItem
from scrapy import Spider, Request
import re


class TournamentsHistorySpider(Spider):
    name = 'tournametsHistory_spider'
    allowed_urls = ['https://www.esportsearnings.com/']
    start_urls = ['https://www.esportsearnings.com/history/2020/list_events']

    def parse(self, response):
        # here I get the href for each year
        years = range(1998, 2021)
        year_urls = [
            f'https://www.esportsearnings.com/history/{year}/list_events' for year in years]

        # go for each year page
        for url in year_urls:
            yield Request(url=url, callback=self.parse_year_page)

    def parse_year_page(self, response):
        year = response.xpath(
            '//h2[@class="detail_box_title"]/text()').extract_first()[-4:]
        totalPrize = float(''.join(re.findall(r'\d+|[.]', response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            0].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first())))
        totalTournaments = response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            1].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first()
        totalActivePlayers = response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            2].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first()
        meanTournamentPrizePool = float(''.join(re.findall(r'\d+|[.]', response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            3].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first())))
        meanEarningsPlayers = float(''.join(re.findall(r'\d+|[.]', response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            4].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first())))
        medianTournamentPrizePool = float(''.join(re.findall(r'\d+|[.]', response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            5].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first())))
        medianEarningsPlayers = float(''.join(re.findall(r'\d+|[.]', response.xpath('// div[@class="info_box_inner"]//div[@class="format_row"]')[
            6].xpath('.//span[@class="format_cell detail_list_prize"]/text()').extract_first())))

        item = TournamentshistoryItem()
        item['year'] = year
        item['totalPrize'] = totalPrize
        item['totalTournaments'] = totalTournaments
        item['totalActivePlayers'] = totalActivePlayers
        item['meanTournamentPrizePool'] = meanTournamentPrizePool
        item['meanEarningsPlayers'] = meanEarningsPlayers
        item['medianTournamentPrizePool'] = medianTournamentPrizePool
        item['medianEarningsPlayers'] = medianEarningsPlayers

        yield item
