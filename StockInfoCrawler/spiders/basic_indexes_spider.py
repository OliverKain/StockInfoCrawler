# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from urllib import parse as urlparse
from StockInfoCrawler.items import BasicIndexesItem


class BasicIndexesSpider(scrapy.Spider):
    name = 'basic-indexes-spider'
    start_urls = ['http://www.cophieu68.vn/companylist2.php']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data/stats/basic-indexes.csv',
    }

    def parse(self, response):
        last_page_xpath = "//ul[@id='navigator']/li[7]/a/@href"
        total_page = int(json.loads(json.dumps(urlparse.parse_qs(
                response.selector.xpath(last_page_xpath).extract_first())))['?currentPage'][0]) + 1
        for i in range(1, total_page, 1):
            page_link = 'http://www.cophieu68.vn/companylist2.php?currentPage=' + str(i)
            yield Request(url=page_link, callback=self.parse_page)

    @staticmethod
    def parse_page(response):
        stock_table_xpath = "//tbody[@id='fred']/tr"
        stock_list = response.selector.xpath(stock_table_xpath)
        stock_list.pop(0)
        for stock in stock_list:
            stock_stat = BasicIndexesItem()
            stock_stat["stock_id"] = extract_str(stock.xpath("./td[2]//strong/text()").extract_first())
            stock_stat["last_close"] = extract_str(stock.xpath("./td[3]//strong/text()").extract_first())
            stock_stat["book_value"] = extract_str(stock.xpath("./td[4]/text()").extract_first())
            stock_stat["highest_52w"] = extract_str(stock.xpath("./td[5]/text()").extract_first())
            stock_stat["lowest_52w"] = extract_str(stock.xpath("./td[6]/text()").extract_first())
            stock_stat["pe"] = extract_str(stock.xpath("./td[7]/text()").extract_first())
            stock_stat["eps"] = extract_str(stock.xpath("./td[8]//strong/text()").extract_first())
            stock_stat["roa"] = extract_str(stock.xpath("./td[9]/text()").extract_first())
            stock_stat["roe"] = extract_str(stock.xpath("./td[10]/text()").extract_first())
            stock_stat["beta"] = extract_str(stock.xpath("./td[11]//strong/text()").extract_first())
            stock_stat["avg_vol_13w"] = extract_str(stock.xpath("./td[12]/text()").extract_first())
            stock_stat["on_bal_vol_ratio"] = extract_str(stock.xpath("./td[13]/text()").extract_first())
            stock_stat["volume"] = extract_str(stock.xpath("./td[14]/text()").extract_first())
            stock_stat["cap_market"] = extract_str(stock.xpath("./td[15]/text()").extract_first())
            yield stock_stat
        pass


def extract_str(xpath):
    regex_valid_data = r'[^A-Za-z0-9\.%]+'
    return re.sub(regex_valid_data, '', xpath)
