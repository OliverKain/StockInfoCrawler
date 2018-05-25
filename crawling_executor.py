# -*- coding: utf-8 -*-

import re
import csv
import numpy
import logging

from commons.clean_crawled_data import clean_up_data
from commons.website_idx_enum import WEBSITE_IDX

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
from StockInfoCrawler.spiders.hnx_spider import HnxSpider
from StockInfoCrawler.spiders.hsx_spider import HsxSpider
from StockInfoCrawler.spiders.nytimes_spider import NYTimesSpider
from StockInfoCrawler.spiders.nguoitieudung_spider import NguoiTieuDungSpider
from StockInfoCrawler.spiders.reuters_spider import ReutersSpider
from StockInfoCrawler.spiders.sbv_spider import SbvSpider
from StockInfoCrawler.spiders.scic_spider import ScicSpider
from StockInfoCrawler.spiders.taichinhdientu_spider import TaiChinhDienTuSpider
from StockInfoCrawler.spiders.theleader_spider import TheLeaderSpider
from StockInfoCrawler.spiders.thoibaonganhang_spider import ThoiBaoNganHangSpider
from StockInfoCrawler.spiders.thoibaotaichinhvietnam_spider import ThoiBaoTaiChinhVietNamSpider
from StockInfoCrawler.spiders.vietnamfinance_spider import VietnamFinanceSpider
from StockInfoCrawler.spiders.vneconomy_spider import VnEconomySpider


# Global variable
is_debug = True
keyword = []
# Clean up data folder
clean_up_data()

availableList = range(1, len(WEBSITE_IDX) + 1)


# Display options
inputOpt = input("Chỉ số cơ bản(s) hay tin tức(n)? [s/n]:")
while inputOpt.lower() != "s" and inputOpt.lower() != "n":
    inputOpt = input("Hãy nhập lại lựa chọn [s/n]:")

# Stats
if inputOpt == "s":
    reqOpt = ["999"]

# News
else:
    print("Lựa chọn hiện có: ")
    print("[{0}] baocongthuong.com.vn".format(WEBSITE_IDX.BAOCONGTHUONG_IDX.value))
    print("[{0}] baodientu.chinhphu.vn".format(WEBSITE_IDX.BAODIENTUCHINHPHU_IDX.value))
    print("[{0}] forbesvietnam.com.vn".format(WEBSITE_IDX.FORBESVIETNAM_IDX.value))
    print("[{0}] hnx.vn (Thông tin công bố HNX)".format(WEBSITE_IDX.HNX_IDX.value))
    print("[{0}] hsx.vn (Thông tin công bố HSX)".format(WEBSITE_IDX.HSX_IDX.value))
    print("[{0}] nguoitieudung.com.vn".format(WEBSITE_IDX.NGUOITIEUDUNG_IDX.value))
    print("[{0}] sbv.gov.vn (Ngân Hàng Nhà Nước)".format(WEBSITE_IDX.SBV_IDX.value))
    print("[{0}] scic.vn (Tổng công ty Đầu tư và kinh doanh vốn nhà nước)".format(WEBSITE_IDX.SCIC_IDX.value))
    print("[{0}] taichinhdientu.vn".format(WEBSITE_IDX.TAICHINHDIENTU_IDX.value))
    print("[{0}] theleader.vn".format(WEBSITE_IDX.THELEADER_IDX.value))
    print("[{0}] thoibaonganhang.vn".format(WEBSITE_IDX.THOIBAONGANHANG_IDX.value))
    print("[{0}] thoibaotaichinhvietnam.vn".format(WEBSITE_IDX.THOIBAOTAICHINHVIETNAM_IDX.value))
    print("[{0}] vneconomy.vn".format(WEBSITE_IDX.VNECONOMY_IDX.value))
    print("[{0}] vietnamfinance.vn".format(WEBSITE_IDX.VIETNAMFINANCE_IDX.value))
    print("[{0}] bloomberg.com".format(WEBSITE_IDX.BLOOMBERG_IDX.value))
    print("[{0}] cnbc.com".format(WEBSITE_IDX.CNBC_IDX.value))
    print("[{0}] reuters.com".format(WEBSITE_IDX.REUTERS_IDX.value))
    print("[{0}] nytimes.com".format(WEBSITE_IDX.NYTIMES_IDX.value))
    print("\n")

    # Prompt spiders
    # TODO Debug Mode
    if is_debug:
        inputOpt = input("Một(s) hay nhiều(m) trang? [s/m]:")
        reqOpt = ""
        while inputOpt.lower() != "s" and inputOpt.lower() != "m":
            inputOpt = input("Hãy nhập lại lựa chọn [s/m]:")
        # Single site
        if inputOpt == "s":
            inputOpt = input("Hãy nhập lựa chọn của bạn [1-" + str(len(availableList)) + "]:")
            while int(inputOpt.lower()) not in availableList:
                inputOpt = input("Hãy nhập lại lựa chọn [1-" + str(len(availableList)) + "]:")
            reqOpt = [int(inputOpt)]
        # Multiple sites
        elif inputOpt == "m":
            inputOpt = input("Hãy nhập danh sách các website muốn lấy, cách nhau bởi dấu phẩy[1-{0}]:"
                                .format(str(len(availableList))))
            while True:
                if re.match(r"^\d(,[\d]+)+$", inputOpt):
                    optList = list(map(int,inputOpt.split(",")))
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

    # Release Mode
    else:
        inputOpt = input("Tin tức trong nước (v) hay thế giới(w)? [v/w]:")
        reqOpt = ""
        while inputOpt.lower() != "v" and inputOpt.lower() != "w":
            inputOpt = input("Hãy nhập lại lựa chọn [v/w]:")
        if inputOpt == "v":
            # VN News
            reqOpt = [WEBSITE_IDX.BAOCONGTHUONG_IDX.value, WEBSITE_IDX.FORBESVIETNAM_IDX.value,
                      WEBSITE_IDX.NGUOITIEUDUNG_IDX.value, WEBSITE_IDX.SCIC_IDX.value,
                      WEBSITE_IDX.THELEADER_IDX.value, WEBSITE_IDX.THOIBAOTAICHINHVIETNAM_IDX.value,
                      WEBSITE_IDX.VIETNAMFINANCE_IDX.value, WEBSITE_IDX.VNECONOMY_IDX.value]
        else:
            # World News
            reqOpt = [WEBSITE_IDX.BLOOMBERG_IDX.value, WEBSITE_IDX.CNBC_IDX.value,
                      WEBSITE_IDX.NYTIMES_IDX.value, WEBSITE_IDX.REUTERS_IDX.value]

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
# TODO Add timestamp filter
if WEBSITE_IDX.BAOCONGTHUONG_IDX.value in reqOpt:
    # TODO Entire page?
    baocongthuong_spider = BaoCongThuongSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(baocongthuong_spider, kw=keyword)
if WEBSITE_IDX.BAODIENTUCHINHPHU_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    process.crawl(BaoDienTuChinhPhuSpider)
if WEBSITE_IDX.FORBESVIETNAM_IDX.value in reqOpt:
    forbesvietnam_spider = ForbesVietNamSpider(kw=keyword)
    # noinspection PyTypeChecker    
    process.crawl(forbesvietnam_spider, kw=keyword)
if WEBSITE_IDX.HNX_IDX.value in reqOpt:
    # TODO iterate sub-menu + paging, 1 exported file
    process.crawl(HnxSpider)
if WEBSITE_IDX.HSX_IDX.value in reqOpt:
    hsx_spider = HsxSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(hsx_spider, kw=keyword)
if WEBSITE_IDX.NGUOITIEUDUNG_IDX.value in reqOpt:
    # TODO Entire page?
    nguoitieudung_spider = NguoiTieuDungSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(nguoitieudung_spider, kw=keyword)
if WEBSITE_IDX.SBV_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    process.crawl(SbvSpider)
if WEBSITE_IDX.SCIC_IDX.value in reqOpt:
    scic_spider = ScicSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(scic_spider, kw=keyword)
if WEBSITE_IDX.TAICHINHDIENTU_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file, display url
    process.crawl(TaiChinhDienTuSpider)
if WEBSITE_IDX.THELEADER_IDX.value in reqOpt:
    theleader_spider = TheLeaderSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(theleader_spider, kw=keyword)
if WEBSITE_IDX.THOIBAONGANHANG_IDX.value in reqOpt:
    thoibaonganhang_spider = ThoiBaoNganHangSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(thoibaonganhang_spider, kw=keyword)
if WEBSITE_IDX.THOIBAOTAICHINHVIETNAM_IDX.value in reqOpt:
    thoibaotaichinhvietnam_spider = ThoiBaoTaiChinhVietNamSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(thoibaotaichinhvietnam_spider, kw=keyword)
if WEBSITE_IDX.VNECONOMY_IDX.value in reqOpt:
    vneconomy_spider = VnEconomySpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(vneconomy_spider, kw=keyword)
if WEBSITE_IDX.VIETNAMFINANCE_IDX.value in reqOpt:
    vietnamfinance_spider = VietnamFinanceSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(vietnamfinance_spider, kw=keyword)

if WEBSITE_IDX.BLOOMBERG_IDX.value in reqOpt:
    bloomberg_spider = BloombergSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(bloomberg_spider, kw=keyword)
if WEBSITE_IDX.CNBC_IDX.value in reqOpt:
    cnbc_spider = CnbcSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(cnbc_spider, kw=keyword)
if WEBSITE_IDX.REUTERS_IDX.value in reqOpt:
    reuters_spider = ReutersSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(reuters_spider, kw=keyword)
if WEBSITE_IDX.NYTIMES_IDX.value in reqOpt:
    nytimes_spider = NYTimesSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(nytimes_spider, kw=keyword)

# Set logging level
# logging.getLogger('scrapy').setLevel(logging.DEBUG)

# Start crawling
process.start()

# TODO http://tapchitaichinh.vn/kinh-te-vi-mo/
# TODO http://tapchitaichinh.vn/thi-truong-tai-chinh/
# TODO http://kinhtevn.com.vn
# TODO http://nhipcaudautu.vn
# TODO http://www.ssc.gov.vn/ubck/faces/vi/vimenu/vipages_vitintucsukien/phathanh
# ?_afrWindowId=y2lp9w8o6_70&_afrLoop=22847863432695794&_afrWindowMode=0&_adf.ctrl-state=1azrsvakbj_4
# #%40%3F_afrWindowId%3Dy2lp9w8o6_70%26_afrLoop%3D22847863432695794%26_afrWindowMode%3D0%26_adf.ctrl-state%3Dy2lp9w8o6_90
# TODO http://enternews.vn
# TODO https://www.hsx.vn/Modules/Cms/Web/NewsByCat/dca0933e-a578-4eaf-8b29-beb4575052c5?rid=1953252732
# TODO http://www.thesaigontimes.vn/kinhdoanh/
# TODO https://www.hsx.vn/Modules/Cms/Web/NewsByCat/dca0933e-a578-4eaf-8b29-beb4575052c5?rid=1500303253
# TODO http://www.mpi.gov.vn/Pages/chuyenmuctin.aspx?idcm=54
# TODO http://www.moit.gov.vn/
# TODO https://hnx.vn/thong-tin-cong-bo-ny-tcph.html


# TODO https://www.dealstreetasia.com/countries/vietnam/
# https://hnx.vn/ModuleArticles/ArticlesCPEtfs/NextPageTinCPNY_CBTCPH?pNumPage=1&pAction=0&pNhomTin=&pTieuDeTin=&pMaChungKhoan=&pFromDate=&pToDate=&pOrderBy=&pNumRecord=100