import os
from scrapy.crawler import CrawlerProcess
from commons.clean_crawled_data import clean_up_data
from scrapy.utils.project import get_project_settings
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


# Clean up data folder
clean_up_data()

# Display options
print("Available crawling: ")
print("[1]  cophieu68.vn: All Basic Indexes")
print("[2]  cophieu68.vn: All Basic Index Power")
print("[3]  cophieu68.vn: All Event Schedule")
print("[4]  vneconomy.vn")
print("[5]  thoibaotaichinhvietnam.vn")
print("[6]  scic.vn (Tổng công ty Đầu tư và kinh doanh vốn nhà nước)")
print("[7]  sbv.gov.vn (Ngân Hàng Nhà Nước)")
print("[8]  taichinhdientu.vn")
print("[9]  baodientu.chinhphu.vn")
print("[10] hnx.vn (Thông tin công bố HNX)")
# http://theleader.vn
# http://vietnamfinance.vn
# http://tapchitaichinh.vn/kinh-te-vi-mo/
# http://tapchitaichinh.vn/thi-truong-tai-chinh/
# http://kinhtevn.com.vn
# http://nhipcaudautu.vn
# http://www.thesaigontimes.vn
# http://www.ssc.gov.vn/ubck/faces/vi/vimenu/vipages_vitintucsukien/phathanh?_afrWindowId=y2lp9w8o6_70&_afrLoop=22847863432695794&_afrWindowMode=0&_adf.ctrl-state=1azrsvakbj_4#%40%3F_afrWindowId%3Dy2lp9w8o6_70%26_afrLoop%3D22847863432695794%26_afrWindowMode%3D0%26_adf.ctrl-state%3Dy2lp9w8o6_90
#
# http://baochinhphu.vn/Kinh-te/7.vgp
# http://enternews.vn
# https://www.hsx.vn/Modules/Cms/Web/NewsByCat/dca0933e-a578-4eaf-8b29-beb4575052c5?rid=1953252732

# Get global project settings
# settings = get_project_settings()

# Create new process
# process = CrawlerProcess(settings)

# Get prompts from screen

# Add spiders
# vneconomySpider = VnEconomySpider()
# process.crawl(vneconomySpider)
# process.crawl(BasicIndexesSpider)
# process.crawl(BasicIndexesPowerSpider)
# process.crawl(EventScheduleSpider)
# process.crawl(ScicPortfolioSpider)
# process.crawl(ScicPressSpider)
# process.crawl(SbvSpider)
# process.crawl(ThoiBaoTaiChinhVietNamSpider)
# process.crawl(TaiChinhDienTuSpider)
# process.crawl(BaoDienTuChinhPhuSpider)
# process.crawl(HnxDisclosureSpider)

# Start crawling
# process.start()
