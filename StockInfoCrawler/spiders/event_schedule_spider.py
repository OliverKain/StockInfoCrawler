# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from urllib import parse as urlparse
from StockInfoCrawler.items import EventDetailItem
from datetime import datetime as dt


class EventScheduleSpider(scrapy.Spider):
    name = 'event-schedule-spider'
    start_urls = ['http://www.cophieu68.vn/events.php?lang=en']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data/stats/events.csv',
    }

    def parse(self, response):
        # last_page_xpath = "//ul[@id='navigator']/li[7]/a/@href"
        # total_page = int(json.loads(json.dumps(urlparse.parse_qs(
        #         response.selector.xpath(last_page_xpath).extract_first())))['?currentPage'][0]) + 1
        total_page = 100
        for i in range(1, total_page, 1):
            page_link = 'http://www.cophieu68.vn/events.php?lang=en&currentPage=' + str(i)
            yield Request(url=page_link, callback=self.parse_page, priority=total_page-i+1)

    @staticmethod
    def parse_page(response):
        stock_table_xpath = "//div[@id='events']/table/tr"
        stock_list = response.selector.xpath(stock_table_xpath)
        stock_list.pop(0)
        for stock in stock_list:
            try:
                exec_date_str = extract_str(stock.xpath("./td[4]/text()").extract_first())
                exec_date = dt.strptime(exec_date_str, "%d/%m/%Y")
                if exec_date < dt.now():
                    continue
                event_detail = EventDetailItem()
                event_detail["stock_id"] = extract_str(stock.xpath("./td[1]//strong/text()").extract_first())
                event_detail["event_type"] = extract_str(stock.xpath("./td[2]/text()").extract_first())
                event_detail["exec_date"] = extract_str(stock.xpath("./td[4]/text()").extract_first())
                event_detail["dividends"] = extract_str(stock.xpath("./td[5]/text()").extract_first())
                event_detail["note"] = stock.xpath("./td[6]/span/text()").extract_first()
                yield event_detail
            except ValueError:
                continue
        pass


def extract_str(xpath):
    regex_valid_data = r'[^A-Za-z0-9\.%/]+'
    return re.sub(regex_valid_data, '', xpath)
