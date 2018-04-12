import os
from scrapy.crawler import CrawlerProcess
from StockInfoCrawler.spiders.basic_indexes_spider import BasicIndexesSpider
from StockInfoCrawler.spiders.basic_indexes_power_spider import BasicIndexesPowerSpider
from StockInfoCrawler.spiders.event_schedule_spider import EventScheduleSpider
from scrapy.utils.project import get_project_settings


if os.path.exists(BasicIndexesSpider.custom_settings["FEED_URI"]):
    os.remove(BasicIndexesSpider.custom_settings["FEED_URI"])
if os.path.exists(BasicIndexesPowerSpider.custom_settings["FEED_URI"]):
    os.remove(BasicIndexesPowerSpider.custom_settings["FEED_URI"])
if os.path.exists(EventScheduleSpider.custom_settings["FEED_URI"]):
    os.remove(EventScheduleSpider.custom_settings["FEED_URI"])

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(BasicIndexesSpider)
process.crawl(BasicIndexesPowerSpider)
process.crawl(EventScheduleSpider)
process.start()