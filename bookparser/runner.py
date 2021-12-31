from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookparser import settings
from bookparser.spiders.labirint import LabirintSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(settings=crawler_setting)
    process.crawl(LabirintSpider)

    process.start()
