import scrapy
from steam_crawler.items import SteamCrawlerItem

queries = ['mmorpg', 'horror', 'anime']


class SteamspiderSpider(scrapy.Spider):
    name = 'SteamSpider'

    def start_requests(self):
        for query in queries:
            for i in range(1, 3):
                url = f'https://store.steampowered.com/search/?term={query}&page={i}&ignore_preferences=1&category1=998'
                yield scrapy.Request(url=url, callback=self.parse_hrefs, flags=[query])

    def parse_hrefs(self, response):
        hrefs = response.xpath('//div[contains(@id, "search_resultsRows")]/a/@href').extract()
        for href in hrefs:
            platforms = response.xpath(
                f'//a[contains(@href, "{href}")]//div[@class="col search_name ellipsis"]/div//span/@class').extract()
            platforms = list(map(lambda x: x.split()[1], platforms))
            yield scrapy.Request(url=href, callback=self.parse_game_page, flags=[response.request.flags[0], platforms])

    def parse_game_page(self, response):
        items = SteamCrawlerItem()
        name = response.xpath('//div[contains(@id, "appHubAppName")]/text()').extract()[0]
        price = ' '.join(response.xpath('//div[contains(@class, "game_purchase_price")]/text()').extract()[0].split())
        cats = response.xpath('//div[@class="blockbg"]//text()').extract()[3:-2:2]
        reviews_list = response.xpath('//div[@class="summary column"]//text()').extract()
        score = reviews_list[1]
        review_number = ' '.join(reviews_list[3].split())[1:-1]
        release_date = response.xpath('//div[@class="date"]/text()').extract()[0]
        developer = response.xpath('//div[contains(@id, "developers_list")]/a/text()').extract()[0]
        tags = list(map(lambda x: ' '.join(x.split()),
                        response.xpath('//div[contains(@class, "glance_tags popular_tags")]//text()').extract()[1:-2]))
        items['name'] = name
        items['query'] = response.request.flags[0]
        items['score'] = score
        items['review_number'] = review_number
        items['developer'] = developer
        items['release_date'] = release_date
        items['categories'] = cats
        items['price'] = price
        items['tags'] = tags
        items['platforms'] = response.request.flags[1]
        yield items
