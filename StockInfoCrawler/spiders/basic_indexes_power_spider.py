# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from urllib import parse as urlparse
from StockInfoCrawler.items import BasicIndexesPowerItem


class BasicIndexesPowerSpider(scrapy.Spider):
    name = 'basic-indexes-power-spider'
    start_urls = ['http://www.cophieu68.vn/investment_basic_indexes.php']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI' : 'data/basic-indexes-power.csv',
    }

    def parse(self, response):
        last_page_xpath = "//ul[@id='navigator']/li[7]/a/@href"
        total_page = int(json.loads(json.dumps(urlparse.parse_qs(
                response.selector.xpath(last_page_xpath).extract_first())))['?currentPage'][0]) + 1
        for i in range(1, total_page, 1):
            page_link = 'http://www.cophieu68.vn/investment_basic_indexes.php?currentPage=' + str(i)
            yield Request(url=page_link, callback=self.parse_page)

    @staticmethod
    def parse_page(response):
        stock_table_xpath = "//tbody[@id='fred']/tr"
        stock_list = response.selector.xpath(stock_table_xpath)
        stock_list.pop(0)
        for stock in stock_list:
            index_powers = BasicIndexesPowerItem()
            index_powers["stock_id"] = extract_str(stock.xpath("./td[2]//strong/text()").extract_first())
            index_powers["eps"] = extract_str(stock.xpath("./td[3]/text()").extract_first())
            index_powers["pe"] = extract_str(stock.xpath("./td[4]/text()").extract_first())
            index_powers["roa"] = extract_str(stock.xpath("./td[5]/text()").extract_first())
            index_powers["roe"] = extract_str(stock.xpath("./td[6]/text()").extract_first())
            index_powers["best_effective"] = len(stock.xpath("./td[7]/i"))
            index_powers["p_on_b"] = extract_str(stock.xpath("./td[8]//text()").extract_first())
            index_powers["stock_at_btm"] = extract_str(stock.xpath("./td[9]/text()").extract_first())
            index_powers["debt_ratio"] = extract_str(stock.xpath("./td[10]/text()").extract_first())
            index_powers["best_value"] = len(stock.xpath("./td[11]/i"))
            index_powers["beta"] = extract_str(stock.xpath("./td[12]/text()").extract_first())
            index_powers["on_bal_vol_ratio"] = extract_str(stock.xpath("./td[13]/text()").extract_first())
            index_powers["best_surf"] = len(stock.xpath("./td[14]/i"))
            index_powers["avg_strength"] = extract_str(stock.xpath("./td[15]//strong/text()").extract_first())
            yield index_powers
        pass


def extract_str(xpath):
    regex_valid_data = r'[^A-Za-z0-9\.%]+'
    return re.sub(regex_valid_data, '', xpath)
