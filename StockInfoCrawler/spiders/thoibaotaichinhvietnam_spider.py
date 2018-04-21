# -*- coding: utf-8 -*-
import scrapy


class ThoiBaoTaiChinhVietNamSpider(scrapy.Spider):
    name = "thoibaotaichinhvietnam-spider"

    # Crawling Info
    target_root = "http://thoibaotaichinhvietnam.vn/pages/chung-khoan-5.aspx"
    list_xpath = "//div[@class='component_content']/div"
    div_class_xpath = "./@class"
    title_xpath = "./div[@class='info_details']/div[@class='title']/div[@class='noindex']/a/text()"
    time_xpath = "./div[@class='info_details']/div[@class='title']/div[@class='noindex']/span/text()"
    intro_xpath = "./div[@class='info_details']/div[@class='introtext']/text()"

    start_urls = ["http://thoibaotaichinhvietnam.vn/pages/chung-khoan-5.aspx"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/thoibaotaichinhvietnam.csv",
    }

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            div_class = str(article.xpath(self.div_class_xpath).extract_first())
            if div_class.find("row") > -1:
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": article.xpath(self.time_xpath).extract_first().strip(),
                                  "intro": article.xpath(self.intro_xpath).extract_first().strip()}
                yield article_detail
