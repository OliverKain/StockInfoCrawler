import os
from scrapy.crawler import CrawlerProcess
from StockInfoCrawler.spiders.basic_indexes_spider import BasicIndexesSpider
from StockInfoCrawler.spiders.basic_indexes_power_spider import BasicIndexesPowerSpider
from StockInfoCrawler.spiders.event_schedule_spider import EventScheduleSpider
from StockInfoCrawler.spiders.vneconomy_spider import VnEconomySpider
from StockInfoCrawler.spiders.scic_portfolio_spider import ScicPortfolioSpider
from StockInfoCrawler.spiders.scic_press_spider import ScicPressSpider
from StockInfoCrawler.spiders.sbv_spider import SbvSpider
from StockInfoCrawler.spiders.thoibaotaichinhvietnam_spider import ThoiBaoTaiChinhVietNamSpider
from StockInfoCrawler.spiders.taichinhdientu_spider import TaiChinhDienTuSpider
from StockInfoCrawler.spiders.baodientuchinhphu_spider import BaoDienTuChinhPhuSpider
from StockInfoCrawler.spiders.hnx_disclosure_spider import HnxDisclosureSpider
from scrapy.utils.project import get_project_settings


if os.path.exists(BasicIndexesSpider.custom_settings["FEED_URI"]):
    os.remove(BasicIndexesSpider.custom_settings["FEED_URI"])
if os.path.exists(BasicIndexesPowerSpider.custom_settings["FEED_URI"]):
    os.remove(BasicIndexesPowerSpider.custom_settings["FEED_URI"])
if os.path.exists(EventScheduleSpider.custom_settings["FEED_URI"]):
    os.remove(EventScheduleSpider.custom_settings["FEED_URI"])
if os.path.exists(VnEconomySpider.custom_settings["FEED_URI"]):
    os.remove(VnEconomySpider.custom_settings["FEED_URI"])
if os.path.exists(ScicPortfolioSpider.custom_settings["FEED_URI"]):
    os.remove(ScicPortfolioSpider.custom_settings["FEED_URI"])
if os.path.exists(ScicPressSpider.custom_settings["FEED_URI"]):
    os.remove(ScicPressSpider.custom_settings["FEED_URI"])
if os.path.exists(SbvSpider.custom_settings["FEED_URI"]):
    os.remove(SbvSpider.custom_settings["FEED_URI"])
if os.path.exists(ThoiBaoTaiChinhVietNamSpider.custom_settings["FEED_URI"]):
    os.remove(ThoiBaoTaiChinhVietNamSpider.custom_settings["FEED_URI"])
if os.path.exists(TaiChinhDienTuSpider.custom_settings["FEED_URI"]):
    os.remove(TaiChinhDienTuSpider.custom_settings["FEED_URI"])
if os.path.exists(BaoDienTuChinhPhuSpider.custom_settings["FEED_URI"]):
    os.remove(BaoDienTuChinhPhuSpider.custom_settings["FEED_URI"])
if os.path.exists(HnxDisclosureSpider.custom_settings["FEED_URI"]):
    os.remove(HnxDisclosureSpider.custom_settings["FEED_URI"])


settings = get_project_settings()
process = CrawlerProcess(settings)

# process.crawl(BasicIndexesSpider)

# process.crawl(BasicIndexesPowerSpider)

# process.crawl(EventScheduleSpider)

# vneconomySpider = VnEconomySpider()
# process.crawl(vneconomySpider)

process.crawl(ScicPortfolioSpider)

process.crawl(ScicPressSpider)

process.crawl(SbvSpider)

process.crawl(ThoiBaoTaiChinhVietNamSpider)

process.crawl(TaiChinhDienTuSpider)

process.crawl(BaoDienTuChinhPhuSpider)

process.crawl(HnxDisclosureSpider)

process.start()
