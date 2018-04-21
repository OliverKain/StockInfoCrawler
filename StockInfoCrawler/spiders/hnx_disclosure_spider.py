# -*- coding: utf-8 -*-
import scrapy


class HnxDisclosureSpider(scrapy.Spider):
    name = "hnx-disclosure-spider"

    # Crawling Info
    target_root = "https://hnx.vn/"
    list_xpath = "//div[@id='divContainTable']/table/tbody/tr"
    stock_id_xpath = "./td[3]/a/text()"
    title_xpath = "./td[4]/a/text()"
    time_xpath = "./td[2]/text()"

    start_urls = ["https://hnx.vn/vi-vn/thong-tin-cong-bo-ny-hnx.html"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/hnx_disclosure.csv",
    }

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            article_detail = {"stock_id": article.xpath(self.stock_id_xpath).extract_first().strip(),
                              "title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": article.xpath(self.time_xpath).extract_first().strip()}
            yield article_detail
