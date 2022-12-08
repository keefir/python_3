# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SteamCrawlerPipeline:
    def open_spider(self, spider): # что делать при открытии паука (создаем файлик)
        self.file = open('games.json', 'w')
        self.basis = {'mmorpg': [], 'horror': [], 'anime': []}

    def close_spider(self, spider): # что делать при окончании работы паука (закрываем файлик)
        self.file.write(json.dumps(self.basis))
        self.file.close()

    def process_item(self, item, spider): # что делать с полученным item
        if int(item['release_date'].split()[-1]) > 2000:
            self.basis[item['query']].append(ItemAdapter(item).asdict())
            return item
