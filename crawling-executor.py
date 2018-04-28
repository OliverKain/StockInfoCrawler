# -*- coding: utf-8 -*-

import re
import csv
import numpy

from commons.clean_crawled_data import clean_up_data

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from StockInfoCrawler.spiders.baodientuchinhphu_spider import BaoDienTuChinhPhuSpider
from StockInfoCrawler.spiders.basic_indexes_power_spider import BasicIndexesPowerSpider
from StockInfoCrawler.spiders.basic_indexes_spider import BasicIndexesSpider
from StockInfoCrawler.spiders.event_schedule_spider import EventScheduleSpider
from StockInfoCrawler.spiders.hnx_disclosure_spider import HnxDisclosureSpider
from StockInfoCrawler.spiders.sbv_spider import SbvSpider
from StockInfoCrawler.spiders.scic_portfolio_spider import ScicPortfolioSpider
from StockInfoCrawler.spiders.scic_press_spider import ScicPressSpider
from StockInfoCrawler.spiders.taichinhdientu_spider import TaiChinhDienTuSpider
from StockInfoCrawler.spiders.thoibaotaichinhvietnam_spider import ThoiBaoTaiChinhVietNamSpider
from StockInfoCrawler.spiders.vneconomy_spider import VnEconomySpider
from StockInfoCrawler.spiders.theleader_spider import TheLeaderSpider
from StockInfoCrawler.spiders.vietnamfinance_spider import VietnamFinanceSpider


# Global variable
keyword = []

# Clean up data folder
clean_up_data()

# Display options
inputOpt = input("Stats or News? [s/n]:")
while inputOpt.lower() != "s" and inputOpt.lower() != "n":
    inputOpt = input("Please enter suitable option [s/n]:")

if inputOpt == "s":
    # Stats
    reqOpt = ["999"]
else:
    # News
    availableList = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    print("Available crawling: ")
    print("[1]  vneconomy.vn")
    print("[2]  thoibaotaichinhvietnam.vn")
    print("[3]  scic.vn (Tổng công ty Đầu tư và kinh doanh vốn nhà nước)")
    print("[4]  sbv.gov.vn (Ngân Hàng Nhà Nước)")
    print("[5]  taichinhdientu.vn")
    print("[6]  baodientu.chinhphu.vn")
    print("[7]  hnx.vn (Thông tin công bố HNX)")
    print("[8]  theleader.vn")
    print("[9]  vietnamfinance.vn\n")

    # Prompt spiders
    inputOpt = input("Single or multiple sites? [s/m]:")
    reqOpt = ""
    while inputOpt.lower() != "s" and inputOpt.lower() != "m":
        inputOpt = input("Please enter suitable option [s/m]:")
    if inputOpt == "s":
        inputOpt = input("Enter site index [1-" + str(len(availableList)) + "]:")
        while inputOpt.lower() not in availableList:
            inputOpt = input("Please enter suitable option [1-" + str(len(availableList)) + "]:")
        reqOpt = [inputOpt]
    else:
        inputOpt = input("Enter list of distinct site indexes, separated by commas [1-"+str(len(availableList))+"]:")
        while True:
            if re.match(r"^\d(,[\d]+)+$", inputOpt):
                optList = inputOpt.split(",")
                if len(numpy.unique(optList)) < len(optList):
                    # Has duplicate options
                    inputOpt = input("Please enter valid list [1-" + str(len(availableList)) + "]:")
                    continue
                for opt in optList:
                    if opt not in availableList:
                        # Invalid options
                        inputOpt = input("Please enter valid list [1-" + str(len(availableList)) + "]:")
                        break
                reqOpt = optList
                break
            else:
                # Invalid list
                inputOpt = input("Please enter valid list [1-" + str(len(availableList)) + "]:")

    # Prompt using keyword
    inputOpt = input("Using keyword [y/n]:")
    while inputOpt.lower() != "y" and inputOpt.lower() != "n":
        inputOpt = input("Please enter suitable option [y/n]:")
    if inputOpt == "y":
        # Prompt using predefined keywords
        inputOpt = input("Using predefined keywords [y/n]:")
        while inputOpt.lower() != "y" and inputOpt.lower() != "n":
            inputOpt = input("Please enter suitable option [y/n]:")
        if inputOpt == "y":
            # Reading keywords
            with open("./input/keyword.csv", "rt", encoding="utf-8") as tmp:
                reader = csv.reader(tmp)
                for row in reader:
                    keyword.append(str(row[0]))
        else:
            # Manual adding keywords
            while True:
                inputOpt = input("Enter keywords, finish adding keywords by typing \"end\":")
                if inputOpt.lower() == "end":
                    break
                keyword.append(inputOpt)

# Get global project settings
settings = get_project_settings()

# Create new process
process = CrawlerProcess(settings)

# Add spiders
# Stats
# TODO single stock_id stats
if "999" in reqOpt:
    process.crawl(BasicIndexesSpider)
    process.crawl(EventScheduleSpider)
    process.crawl(BasicIndexesPowerSpider)

# News
if "1" in reqOpt:
    vneconomy_spider = VnEconomySpider(kw=keyword)
    process.crawl(vneconomy_spider, kw=keyword)
if "2" in reqOpt:
    # TODO iterate sub-menu
    process.crawl(ThoiBaoTaiChinhVietNamSpider)
if "3" in reqOpt:
    # TODO iterate sub-menu
    process.crawl(ScicPortfolioSpider)
    process.crawl(ScicPressSpider)
if "4" in reqOpt:
    # TODO iterate sub-menu
    process.crawl(SbvSpider)
if "5" in reqOpt:
    # TODO iterate sub-menu
    process.crawl(TaiChinhDienTuSpider)
if "6" in reqOpt:
    # TODO iterate sub-menu
    process.crawl(BaoDienTuChinhPhuSpider)
if "7" in reqOpt:
    # TODO iterate sub-menu + paging
    process.crawl(HnxDisclosureSpider)
if "8" in reqOpt:
    theleader_spider = TheLeaderSpider(kw=keyword)
    process.crawl(theleader_spider, kw=keyword)
if "9" in reqOpt:
    vietnamfinance_spider = VietnamFinanceSpider(kw=keyword)
    process.crawl(vietnamfinance_spider, kw=keyword)

# Start crawling
process.start()


# http://tapchitaichinh.vn/kinh-te-vi-mo/
# http://tapchitaichinh.vn/thi-truong-tai-chinh/
# http://kinhtevn.com.vn
# http://nhipcaudautu.vn
# http://www.thesaigontimes.vn
# http://www.ssc.gov.vn/ubck/faces/vi/vimenu/vipages_vitintucsukien/phathanh?_afrWindowId=y2lp9w8o6_70&_afrLoop=22847863432695794&_afrWindowMode=0&_adf.ctrl-state=1azrsvakbj_4#%40%3F_afrWindowId%3Dy2lp9w8o6_70%26_afrLoop%3D22847863432695794%26_afrWindowMode%3D0%26_adf.ctrl-state%3Dy2lp9w8o6_90
# http://baochinhphu.vn/Kinh-te/7.vgp
# http://enternews.vn
# https://www.hsx.vn/Modules/Cms/Web/NewsByCat/dca0933e-a578-4eaf-8b29-beb4575052c5?rid=1953252732
