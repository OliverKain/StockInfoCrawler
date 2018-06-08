# -*- coding: utf-8 -*-
import scrapy
from commons.is_in_filtered_time import is_in_filtered_time


class AcbsSpider(scrapy.Spider):
    name = "acbs-spider"

    # Crawling Info
    max_depth = 5
    target_root = "http://acbs.com.vn"
    company_list_xpath = "//ul[@class='list-data-verticle list-report ']/li"
    company_title_xpath = "./a/span/strong/text()"
    company_time_xpath = "./a/span/small/text()"
    company_link_xpath = "./a/@href"
    market_list_xpath = "//ul[@class='list-news']"
    market_top_title_xpath = "./h4/a/text()"
    market_top_time_xpath = "./p[@class='date-posted']/text()"
    market_top_link_xpath = "./h4/a/@href"
    market_title_xpath = "./div/h4/a/text()"
    market_time_xpath = "./div/p[@class='date-posted']/text()"
    market_link_xpath = "./div/a/@href"
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/acbs.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, mode, **kwargs):
        self.mode = mode
        if self.mode == "c":
            for s in range(1, self.max_depth + 1):
                self.start_urls.append("http://acbs.com.vn/danh-muc/87/bao-cao-doanh-nghiep?page={0}".format(s))
        else:
            for s in range(1, self.max_depth + 1):
                self.start_urls.append("http://acbs.com.vn/danh-muc/70-morning-cafe-news?page={0}".format(s))
        super().__init__(**kwargs)
    
    def parse(self, response):
        if self.mode == "c":
            article_list = response.xpath(self.company_list_xpath)
            for article in article_list:
                time_str = get_time(article.xpath(self.company_time_xpath).extract_first().strip()[-10:])
                if is_in_filtered_time(time_str):
                    article_detail = {
                        "title": article.xpath(self.company_title_xpath).extract_first().strip(),
                        "time": time_str,
                        "link": self.target_root + article.xpath(self.company_link_xpath).extract_first().strip()}
                    yield article_detail
        else:
            market_list = response.xpath(self.market_list_xpath)
            if response.request.url.find("?page=1") > -1:
                for article in market_list[0].xpath("./li"):
                    time_str = get_time(article.xpath(self.market_top_time_xpath).extract_first().strip())
                    if is_in_filtered_time(time_str):
                        article_detail = {
                            "title": article.xpath(self.market_top_title_xpath).extract_first().strip() + " " + time_str,
                            "time": time_str,
                            "link": self.target_root + article.xpath(self.market_top_link_xpath).extract_first().strip()}
                        yield article_detail
            for article in market_list[1].xpath("./li"):
                time_str = get_time(article.xpath(self.market_time_xpath).extract_first().strip())
                if is_in_filtered_time(time_str):
                    article_detail = {
                        "title": article.xpath(self.market_title_xpath).extract_first().strip() + " " + time_str,
                        "time": time_str,
                        "link": self.target_root + article.xpath(self.market_link_xpath).extract_first().strip()}
                    yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
