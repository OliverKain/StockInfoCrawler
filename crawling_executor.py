# -*- coding: utf-8 -*-

import re
import csv
import numpy
import logging

from commons.clean_crawled_data import clean_up_data
from commons.website_idx_enum import WebsiteIdx

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from StockInfoCrawler.spiders.acbs_spider import AcbsSpider
from StockInfoCrawler.spiders.baocongthuong_spider import BaoCongThuongSpider
from StockInfoCrawler.spiders.baodientuchinhphu_spider import BaoDienTuChinhPhuSpider
from StockInfoCrawler.spiders.basic_indexes_power_spider import BasicIndexesPowerSpider
from StockInfoCrawler.spiders.basic_indexes_spider import BasicIndexesSpider
from StockInfoCrawler.spiders.bloomberg_spider import BloombergSpider
from StockInfoCrawler.spiders.bsc_spider import BscSpider
from StockInfoCrawler.spiders.bvsc_spider import BvscSpider
from StockInfoCrawler.spiders.cnbc_spider import CnbcSpider
from StockInfoCrawler.spiders.enternews_spider import EnterNewsSpider
from StockInfoCrawler.spiders.event_schedule_spider import EventScheduleSpider
from StockInfoCrawler.spiders.forbesvietnam_spider import ForbesVietNamSpider
from StockInfoCrawler.spiders.hnx_spider import HnxSpider
from StockInfoCrawler.spiders.hsx_spider import HsxSpider
from StockInfoCrawler.spiders.mbs_spider import MbsSpider
from StockInfoCrawler.spiders.nytimes_spider import NYTimesSpider
from StockInfoCrawler.spiders.nguoitieudung_spider import NguoiTieuDungSpider
from StockInfoCrawler.spiders.reuters_spider import ReutersSpider
from StockInfoCrawler.spiders.sbv_spider import SbvSpider
from StockInfoCrawler.spiders.scic_spider import ScicSpider
from StockInfoCrawler.spiders.taichinhdientu_spider import TaiChinhDienTuSpider
from StockInfoCrawler.spiders.theleader_spider import TheLeaderSpider
from StockInfoCrawler.spiders.thoibaonganhang_spider import ThoiBaoNganHangSpider
from StockInfoCrawler.spiders.thoibaotaichinhvietnam_spider import ThoiBaoTaiChinhVietNamSpider
from StockInfoCrawler.spiders.vcbs_spider import VcbsSpider
from StockInfoCrawler.spiders.vcsc_spider import VcscSpider
from StockInfoCrawler.spiders.vietnamfinance_spider import VietnamFinanceSpider
from StockInfoCrawler.spiders.vneconomy_spider import VnEconomySpider

# <editor-fold desc="">
# </editor-fold>

# <editor-fold desc="GLOBAL VARIABLES">
is_debug = True
keyword = []
report_mode = ""
availableList = range(1, len(WebsiteIdx) + 1)
# </editor-fold>

# <editor-fold desc="GET REQUESTS">
# Clean up data folder
clean_up_data()

# <editor-fold desc="Display available options">
print("Lựa chọn hiện có: ")

# Vietnamese websites
print("[{0}] acbs.com.vn (Công ty chứng khoán ACBS)"
      .format(WebsiteIdx.ACBS_IDX.value))
print("[{0}] baocongthuong.com.vn"
      .format(WebsiteIdx.BAOCONGTHUONG_IDX.value))
print("[{0}] baodientu.chinhphu.vn"
      .format(WebsiteIdx.BAODIENTUCHINHPHU_IDX.value))
print("[{0}] bsc.com.vn (Công ty chứng khoán BIDV)"
      .format(WebsiteIdx.BSC_IDX.value))
print("[{0}] bvsc.com.vn (Công ty chứng khoán Bảo Việt)"
      .format(WebsiteIdx.BVSC_IDX.value))
print("[{0}] enternews.com.vn"
      .format(WebsiteIdx.ENTERNEWS_IDX.value))
print("[{0}] forbesvietnam.com.vn"
      .format(WebsiteIdx.FORBESVIETNAM_IDX.value))
print("[{0}] hnx.vn (Thông tin công bố HNX)"
      .format(WebsiteIdx.HNX_IDX.value))
print("[{0}] hsx.vn (Thông tin công bố HSX)"
      .format(WebsiteIdx.HSX_IDX.value))
print("[{0}] mbs.vn (Công ty chứng khoán MB)"
      .format(WebsiteIdx.MBS_IDX.value))
print("[{0}] nguoitieudung.com.vn"
      .format(WebsiteIdx.NGUOITIEUDUNG_IDX.value))
print("[{0}] sbv.gov.vn (Ngân Hàng Nhà Nước)"
      .format(WebsiteIdx.SBV_IDX.value))
print("[{0}] scic.vn (Tổng công ty Đầu tư và kinh doanh vốn nhà nước)"
      .format(WebsiteIdx.SCIC_IDX.value))
print("[{0}] taichinhdientu.vn"
      .format(WebsiteIdx.TAICHINHDIENTU_IDX.value))
print("[{0}] theleader.vn"
      .format(WebsiteIdx.THELEADER_IDX.value))
print("[{0}] thoibaonganhang.vn"
      .format(WebsiteIdx.THOIBAONGANHANG_IDX.value))
print("[{0}] thoibaotaichinhvietnam.vn"
      .format(WebsiteIdx.THOIBAOTAICHINHVIETNAM_IDX.value))
print("[{0}] vcbs.com.vn (Công ty chứng khoán VCB)"
      .format(WebsiteIdx.VCBS_IDX.value))
print("[{0}] vcsc.com.vn (Viet Capital Securities)"
      .format(WebsiteIdx.VCSC_IDX.value))
print("[{0}] vietnamfinance.vn"
      .format(WebsiteIdx.VIETNAMFINANCE_IDX.value))
print("[{0}] vneconomy.vn"
      .format(WebsiteIdx.VNECONOMY_IDX.value))

# International websites
print("[{0}] bloomberg.com"
      .format(WebsiteIdx.BLOOMBERG_IDX.value))
print("[{0}] cnbc.com"
      .format(WebsiteIdx.CNBC_IDX.value))
print("[{0}] reuters.com"
      .format(WebsiteIdx.REUTERS_IDX.value))
print("[{0}] nytimes.com"
      .format(WebsiteIdx.NYTIMES_IDX.value))

print("\n")
# </editor-fold>

# Debug Mode
if is_debug:
    inputOpt = input("Một(s) hay nhiều(m) trang? [s/m]:")
    reqOpt = ""
    while inputOpt.lower() != "s" and inputOpt.lower() != "m":
        inputOpt = input("Hãy nhập lại lựa chọn [s/m]:")
    # Single site
    if inputOpt == "s":
        inputOpt = input("Hãy nhập lựa chọn của bạn [1-" + str(len(availableList)) + "]:")
        while True:
            # Convert into integer
            try:
                inputOpt_str = int(inputOpt.lower())
            except ValueError:
                inputOpt = input("Hãy nhập lại lựa chọn [1-" + str(len(availableList)) + "]:")
                continue
            # Check if inputted index existed in provided list
            if inputOpt_str not in availableList:
                inputOpt = input("Hãy nhập lại lựa chọn [1-" + str(len(availableList)) + "]:")
            else:
                # Get inputted index
                reqOpt = [int(inputOpt)]
                break
    # Multiple sites
    else:
        inputOpt = input("Hãy nhập danh sách các website muốn lấy, cách nhau bởi dấu phẩy[1-{0}]:"
                            .format(str(len(availableList))))
        while True:
            # RegEx checks inputted list
            if re.match(r"^\d(,[\d]+)+$", inputOpt):
                optList = list(map(int, inputOpt.split(",")))
                # Check duplicate indexes
                if len(numpy.unique(optList)) < len(optList):
                    inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
                    continue
                # Check if inputted index existed in provided list
                is_existed = True
                for opt in optList:
                    if opt not in availableList:
                        # Invalid options
                        inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
                        is_existed = False
                        break
                # Get inputted index list
                if is_existed:
                    reqOpt = optList
                    break
            else:
                # Invalid list
                inputOpt = input("Hãy nhập danh sách đúng qui cách [1-" + str(len(availableList)) + "]:")
# Release Mode
else:
    inputOpt = input("Báo cáo (r) hay Tin tức (n) [r/n]:")
    while inputOpt.lower() != "r" and inputOpt.lower() != "n":
        inputOpt = input("Hãy nhập lại lựa chọn [r/n]:")
    # Reports
    if inputOpt == "r":
        inputOpt = input("Báo cáo công ty (c) hay Báo cáo thị trường(m) [c/m]:")
        while inputOpt.lower() != "c" and inputOpt.lower() != "m":
            inputOpt = input("Hãy nhập lại lựa chọn [c/m]:")
        report_mode = inputOpt
        reqOpt = [WebsiteIdx.ACBS_IDX.value,
                  WebsiteIdx.BSC_IDX.value,
                  WebsiteIdx.BVSC_IDX.value,
                  WebsiteIdx.MBS_IDX.value,
                  WebsiteIdx.VCBS_IDX.value,
                  WebsiteIdx.VCSC_IDX.value]
    # News
    else:
        inputOpt = input("Trong nước (v) hay Thế giới(w)? [v/w]:")
        reqOpt = ""
        while inputOpt.lower() != "v" and inputOpt.lower() != "w":
            inputOpt = input("Hãy nhập lại lựa chọn [v/w]:")
        if inputOpt == "v":
            # VN News
            reqOpt = [WebsiteIdx.BAOCONGTHUONG_IDX.value,
                      WebsiteIdx.FORBESVIETNAM_IDX.value,
                      WebsiteIdx.ENTERNEWS_IDX.value,
                      WebsiteIdx.NGUOITIEUDUNG_IDX.value,
                      # WebsiteIdx.SCIC_IDX.value
                      WebsiteIdx.HNX_IDX.value,
                      WebsiteIdx.HSX_IDX.value,
                      WebsiteIdx.THELEADER_IDX.value,
                      WebsiteIdx.THOIBAONGANHANG_IDX.value,
                      WebsiteIdx.THOIBAOTAICHINHVIETNAM_IDX.value,
                      WebsiteIdx.VIETNAMFINANCE_IDX.value,
                      WebsiteIdx.VNECONOMY_IDX.value]
        else:
            # World News
            reqOpt = [WebsiteIdx.BLOOMBERG_IDX.value,
                      WebsiteIdx.CNBC_IDX.value,
                      WebsiteIdx.NYTIMES_IDX.value,
                      WebsiteIdx.REUTERS_IDX.value]

# TODO Comment for testing
# # Prompt using keyword
# inputOpt = input("Bạn có muốn sử dụng keyword? [y/n]:")
# while inputOpt.lower() != "y" and inputOpt.lower() != "n":
#     inputOpt = input("Hãy nhập lại lựa chọn [y/n]:")
# if inputOpt == "y":
#     # Using keywords
#     inputOpt = input("Có sử dụng các keyword đã định nghĩa sẵn trong input/keyword.csv? [y/n]:")
#     while inputOpt.lower() != "y" and inputOpt.lower() != "n":
#         inputOpt = input("Hãy nhập lại lựa chọn [y/n]:")
#     # Using predefined keywords
#     if inputOpt == "y":
#         with open("./input/keywords.csv", "rt", encoding="utf-8") as tmp:
#             reader = csv.reader(tmp)
#             for row in reader:
#                 keyword.append(str(row[0]))
#     # Manual adding keywords
#     else:
#         while True:
#             inputOpt = input("Hãy nhập các keyword, kết thúc keyword bằng Enter,"
#                               + "hoàn thành việc nhập bằng cách nhập từ \"end\":")
#             if inputOpt.lower() == "end":
#                 break
#             keyword.append(inputOpt)

# Create crawling process (with setting)
settings = get_project_settings()
process = CrawlerProcess(settings)
# </editor-fold>

# <editor-fold desc="CRAWLING PROCESS">
# Stats
# TODO single stock_id stats
if "999" in reqOpt:
    process.crawl(BasicIndexesSpider)
    process.crawl(EventScheduleSpider)
    process.crawl(BasicIndexesPowerSpider)

# Reports
if WebsiteIdx.ACBS_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(AcbsSpider, mode=report_mode)
if WebsiteIdx.BSC_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(BscSpider, mode=report_mode)
if WebsiteIdx.BVSC_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(BvscSpider, mode=report_mode)
if WebsiteIdx.HNX_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(HnxSpider, mode=report_mode)
if WebsiteIdx.HSX_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(HsxSpider, mode=report_mode)
if WebsiteIdx.MBS_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(MbsSpider, mode=report_mode)
if WebsiteIdx.VCBS_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(VcbsSpider, mode=report_mode)
if WebsiteIdx.VCSC_IDX.value in reqOpt:
    # noinspection PyTypeChecker
    process.crawl(VcscSpider, mode=report_mode)

# News
# Vietnamese websites
if WebsiteIdx.BAOCONGTHUONG_IDX.value in reqOpt:
    # TODO Entire page?
    baocongthuong_spider = BaoCongThuongSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(baocongthuong_spider, kw=keyword)
if WebsiteIdx.BAODIENTUCHINHPHU_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    # TODO Add timestamp filter
    process.crawl(BaoDienTuChinhPhuSpider)
if WebsiteIdx.ENTERNEWS_IDX.value in reqOpt:
    enternews_spider = EnterNewsSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(enternews_spider, kw=keyword)
if WebsiteIdx.FORBESVIETNAM_IDX.value in reqOpt:
    forbesvietnam_spider = ForbesVietNamSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(forbesvietnam_spider, kw=keyword)
if WebsiteIdx.NGUOITIEUDUNG_IDX.value in reqOpt:
    # TODO Entire page?
    nguoitieudung_spider = NguoiTieuDungSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(nguoitieudung_spider, kw=keyword)
if WebsiteIdx.SBV_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file
    # TODO Add timestamp filter
    process.crawl(SbvSpider)
if WebsiteIdx.SCIC_IDX.value in reqOpt:
    # TODO Add timestamp filter
    scic_spider = ScicSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(scic_spider, kw=keyword)
if WebsiteIdx.TAICHINHDIENTU_IDX.value in reqOpt:
    # TODO iterate sub-menu, 1 exported file, display url
    # TODO Add timestamp filter
    process.crawl(TaiChinhDienTuSpider)
if WebsiteIdx.THELEADER_IDX.value in reqOpt:
    theleader_spider = TheLeaderSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(theleader_spider, kw=keyword)
if WebsiteIdx.THOIBAONGANHANG_IDX.value in reqOpt:
    thoibaonganhang_spider = ThoiBaoNganHangSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(thoibaonganhang_spider, kw=keyword)
if WebsiteIdx.THOIBAOTAICHINHVIETNAM_IDX.value in reqOpt:
    thoibaotaichinhvietnam_spider = ThoiBaoTaiChinhVietNamSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(thoibaotaichinhvietnam_spider, kw=keyword)
if WebsiteIdx.VIETNAMFINANCE_IDX.value in reqOpt:
    vietnamfinance_spider = VietnamFinanceSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(vietnamfinance_spider, kw=keyword)
if WebsiteIdx.VNECONOMY_IDX.value in reqOpt:
    vneconomy_spider = VnEconomySpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(vneconomy_spider, kw=keyword)
# International websites
if WebsiteIdx.BLOOMBERG_IDX.value in reqOpt:
    bloomberg_spider = BloombergSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(bloomberg_spider, kw=keyword)
if WebsiteIdx.CNBC_IDX.value in reqOpt:
    cnbc_spider = CnbcSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(cnbc_spider, kw=keyword)
if WebsiteIdx.REUTERS_IDX.value in reqOpt:
    reuters_spider = ReutersSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(reuters_spider, kw=keyword)
if WebsiteIdx.NYTIMES_IDX.value in reqOpt:
    nytimes_spider = NYTimesSpider(kw=keyword)
    # noinspection PyTypeChecker
    process.crawl(nytimes_spider, kw=keyword)

# Set logging level
logging.getLogger('scrapy').setLevel(logging.DEBUG)

# Start crawling
process.start()
# </editor-fold>

# TODO http://tapchitaichinh.vn/kinh-te-vi-mo/
# TODO http://tapchitaichinh.vn/thi-truong-tai-chinh/
# TODO http://kinhtevn.com.vn
# TODO http://nhipcaudautu.vn
# TODO http://www.ssc.gov.vn/ubck/faces/vi/vimenu/vipages_vitintucsukien/phathanh
# ?_afrWindowId=y2lp9w8o6_70&_afrLoop=22847863432695794&_afrWindowMode=0&_adf.ctrl-state=1azrsvakbj_4
# #%40%3F_afrWindowId%3Dy2lp9w8o6_70%26_afrLoop%3D22847863432695794%26_afrWindowMode%3D0%26_adf.ctrl-state%3Dy2lp9w8o6_90
# TODO http://www.thesaigontimes.vn/kinhdoanh/
# TODO http://www.mpi.gov.vn/Pages/chuyenmuctin.aspx?idcm=54
# TODO http://www.moit.gov.vn/
# TODO https://hnx.vn/thong-tin-cong-bo-ny-tcph.html


# TODO https://www.dealstreetasia.com/countries/vietnam/
