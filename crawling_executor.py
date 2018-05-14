# -*- coding: utf-8 -*-

import re
import csv
import numpy

from commons.clean_crawled_data import clean_up_data

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from StockInfoCrawler.spiders.baocongthuong_spider import BaoCongThuongSpider
from StockInfoCrawler.spiders.baodientuchinhphu_spider import BaoDienTuChinhPhuSpider
from StockInfoCrawler.spiders.basic_indexes_power_spider import BasicIndexesPowerSpider
from StockInfoCrawler.spiders.basic_indexes_spider import BasicIndexesSpider
from StockInfoCrawler.spiders.bloomberg_spider import BloombergSpider
from StockInfoCrawler.spiders.cnbc_spider import CnbcSpider
from StockInfoCrawler.spiders.event_schedule_spider import EventScheduleSpider
from StockInfoCrawler.spiders.forbesvietnam_spider import ForbesVietNamSpider
from StockInfoCrawler.spiders.hnx_disclosure_spider import HnxDisclosureSpider
from StockInfoCrawler.spiders.nguoitieudung_spider import NguoiTieuDungSpider
from StockInfoCrawler.spiders.reuters_spider import ReutersSpider
from StockInfoCrawler.spiders.sbv_spider import SbvSpider
from StockInfoCrawler.spiders.scic_spider import ScicSpider
from StockInfoCrawler.spiders.taichinhdientu_spider import TaiChinhDienTuSpider
from StockInfoCrawler.spiders.theleader_spider import TheLeaderSpider
from StockInfoCrawler.spiders.thoibaotaichinhvietnam_spider import ThoiBaoTaiChinhVietNamSpider
from StockInfoCrawler.spiders.vietnamfinance_spider import VietnamFinanceSpider
from StockInfoCrawler.spiders.vneconomy_spider import VnEconomySpider


# Global variable
is_debug = False
keyword = []

# Clean up data folder
clean_up_data()

# Display options
inputOpt = input("Chỉ số cơ bản(s) hay tin tức(n)? [s/n]:")
while inputOpt.lower() != "s" and inputOpt.lower() != "n":
    inputOpt = input("Hãy nhập lại lựa chọn [s/n]:")

# Stats
if inputOpt == "s":
    reqOpt = ["999"]

# News
else:
    availableList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                     "11", "12", "13", "14", "15"]
    print("Lựa chọn hiện có: ")
    print("[1]  vneconomy.vn")
    print("[2]  thoibaotaichinhvietnam.vn")
    print("[3]  scic.vn (Tổng công ty Đầu tư và kinh doanh vốn nhà nước)")
    print("[4]  sbv.gov.vn (Ngân Hàng Nhà Nước)")
    print("[5]  taichinhdientu.vn")
    print("[6]  baodientu.chinhphu.vn")
    print("[7]  hnx.vn (Thông tin công bố HNX)")
    print("[8]  theleader.vn")
    print("[9]  vietnamfinance.vn")
    print("[10] nguoitieudung.com.vn")
    print("[11] baocongthuong.com.vn")
    print("[12] forbesvietnam.com.vn")
    print("[13] bloomberg.com")
    print("[14] cnbc.com")
    print("[15] reuters.com")
    print("\n")

    # Prompt spiders
    # TODO Debug Mode
    if is_debug:
        inputOpt = input("Một(s) hay nhiều(m) hay toàn bộ các trang(a)? [s/m/a]:")
        reqOpt = ""
        while inputOpt.lower() != "s" and inputOpt.lower() != "m" and inputOpt.lower() != "a":
            inputOpt = input("Hãy nhập lại lựa chọn [s/m/a]:")
        # Single site
        if inputOpt == "s":
            inputOpt = input("Hãy nhập lựa chọn của bạn [1-" + str(len(availableList)) + "]:")
            while inputOpt.lower() not in availableList:
                inputOpt = input("Hãy nhập lại lựa chọn [1-" + str(len(availableList)) + "]:")
            reqOpt = [inputOpt]
        # Multiple sites
        elif inputOpt == "m":
            inputOpt = input("Hãy nhập danh sách các website muốn lấy, cách nhau bởi dấu phẩy[1-{0}]:"
                                .format(str(len(availableList))))
            while True:
                if re.match(r"^\d(,[\d]+)+$", inputOpt):
                    optList = inputOpt.split(",")
                    if len(numpy.unique(optList)) < len(optList):
                        # Has duplicate options
                        inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
                        continue
                    for opt in optList:
                        if opt not in availableList:
                            # Invalid options
                            inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
                            break
                    reqOpt = optList
                    break
                else:
                    # Invalid list
                    inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
        # All sites
        else:
            reqOpt = availableList
            reqOpt = ["1", "2", "3", "8", "9", "10", "11", "12"]

    # Release Mode
    else:
        inputOpt = input("Tin tức trong nước (v) hay thế giới(w)? [v/w]:")
        reqOpt = ""
        while inputOpt.lower() != "v" and inputOpt.lower() != "w":
            inputOpt = input("Hãy nhập lại lựa chọn [v/w]:")
        if inputOpt == "v":
            # VN News
            reqOpt = ["1", "2", "3", "8", "9", "10", "11", "12"]
        else:
            # World News
            reqOpt = ["14", "15"]

    # Prompt using keyword
    inputOpt = input("Bạn có muốn sử dụng keyword? [y/n]:")
    while inputOpt.lower() != "y" and inputOpt.lower() != "n":
        inputOpt = input("Hãy nhập lại lựa chọn [y/n]:")
    # Using keywords
    if inputOpt == "y":
        inputOpt = input("Có sử dụng các keyword đã định nghĩa sẵn trong input/keyword.csv? [y/n]:")
        while inputOpt.lower() != "y" and inputOpt.lower() != "n":
            inputOpt = input("Hãy nhập lại lựa chọn [y/n]:")
        # Using predefined keywords
        if inputOpt == "y":
            with open("./input/keywords.csv", "rt", encoding="utf-8") as tmp:
                reader = csv.reader(tmp)
                for row in reader:
                    keyword.append(str(row[0]))
        # Manual adding keywords
        else:
            while True:
                inputOpt = input("Hãy nhập các keyword, kết thúc keyword bằng Enter,"
                                  + "hoàn thành việc nhập bằng cách nhập từ \"end\":")
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
    thoibaotaichinhvietnam_spider = ThoiBaoTaiChinhVietNamSpider(kw=keyword)
    process.crawl(thoibaotaichinhvietnam_spider, kw=keyword)
if "3" in reqOpt:
    scic_spider = ScicSpider(kw=keyword)
    process.crawl(scic_spider, kw=keyword)
if "4" in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    process.crawl(SbvSpider)
if "5" in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    process.crawl(TaiChinhDienTuSpider)
if "6" in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    process.crawl(BaoDienTuChinhPhuSpider)
if "7" in reqOpt:
    # TODO iterate sub-menu + paging, 1 exported file
    process.crawl(HnxDisclosureSpider)
if "8" in reqOpt:
    theleader_spider = TheLeaderSpider(kw=keyword)
    process.crawl(theleader_spider, kw=keyword)
if "9" in reqOpt:
    vietnamfinance_spider = VietnamFinanceSpider(kw=keyword)
    process.crawl(vietnamfinance_spider, kw=keyword)
if "10" in reqOpt:
    # TODO Entire page?
    nguoitieudung_spider = NguoiTieuDungSpider(kw=keyword)
    process.crawl(nguoitieudung_spider, kw=keyword)
if "11" in reqOpt:
    # TODO Entire page?
    baocongthuong_spider = BaoCongThuongSpider(kw=keyword)
    process.crawl(baocongthuong_spider, kw=keyword)
if "12" in reqOpt:
    forbesvietnam_spider = ForbesVietNamSpider(kw=keyword)
    process.crawl(forbesvietnam_spider, kw=keyword)
if "13" in reqOpt:
    bloomberg_spider = BloombergSpider(kw=keyword)
    process.crawl(bloomberg_spider, kw=keyword)
if "14" in reqOpt:
    cnbc_spider = CnbcSpider(kw=keyword)
    process.crawl(cnbc_spider, kw=keyword)
if "15" in reqOpt:
    reuters_spider = ReutersSpider(kw=keyword)
    process.crawl(reuters_spider, kw=keyword)

# Start crawling
process.start()

# http://tapchitaichinh.vn/kinh-te-vi-mo/
# http://tapchitaichinh.vn/thi-truong-tai-chinh/
# http://kinhtevn.com.vn
# http://nhipcaudautu.vn
# http://www.ssc.gov.vn/ubck/faces/vi/vimenu/vipages_vitintucsukien/phathanh?_afrWindowId=y2lp9w8o6_70&_afrLoop=22847863432695794&_afrWindowMode=0&_adf.ctrl-state=1azrsvakbj_4#%40%3F_afrWindowId%3Dy2lp9w8o6_70%26_afrLoop%3D22847863432695794%26_afrWindowMode%3D0%26_adf.ctrl-state%3Dy2lp9w8o6_90
# http://enternews.vn
# https://www.hsx.vn/Modules/Cms/Web/NewsByCat/dca0933e-a578-4eaf-8b29-beb4575052c5?rid=1953252732
# http://www.thesaigontimes.vn/kinhdoanh/

# TODO https://www.dealstreetasia.com/countries/vietnam/
# TODO https://www.bloomberg.com/markets
# TODO https://www.bloomberg.com/businessweek
# TODO https://www.reuters.com/news/archive/marketsNews?view=page&page=50
# TODO https://www.nytimes.com/section/business/dealbook?action=click&contentCollection=Business%2FDealBook&contentPlacement=2&module=SectionsNav&pgtype=sectionfront&region=TopBar&version=BrowseTree
