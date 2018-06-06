# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import html
from commons.is_in_filtered_time import is_in_filtered_time


class AcbsSpider(scrapy.Spider):
    name = "acbs-spider"

    # Crawling Info
    max_depth = 5
    target_root = "http://acbs.com.vn"
    list_xpath = "//ul[@class='list-data-verticle list-report ']/li"
    title_xpath = "./a/span/strong/text()"
    time_xpath = "./a/span/small/text()"
    link_xpath = "./a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("http://acbs.com.vn/danh-muc/87/bao-cao-doanh-nghiep?page={0}".format(s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/acbs.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }
    
    def parse(self, response):
        article_list = response.xpath(self.list_xpath)
        for article in article_list:
            time_str = get_time(article.xpath(self.time_xpath).extract_first().strip()[-10:])
            if is_in_filtered_time(time_str):
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": time_str,
                                  "link": self.target_root + article.xpath(self.link_xpath).extract_first().strip()}
                yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]