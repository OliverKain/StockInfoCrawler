# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.http import Request
from addon.no_accent import no_accent_vietnamese


class VnEconomySpider(scrapy.Spider):
    name = "vneconomy-spider"

    # Crawling Info
    target_root = "http://vneconomy.vn"
    article_title_xpath = "./div/h3/a/text()"
    time_xpath = "./div//span[@class='infonews-time']/text()"
    init_xpath = "./div//p/text()"
    link_xpath = "./div/h3/a/@href"

    # Get keyword
    with open("./input/keyword.csv", "rt", encoding="utf-8") as tmp:
        reader = csv.reader(tmp)
        for row in reader:
            keyword = str(row[0])

    start_urls = ["http://vneconomy.vn/timeline/9920/trang-1.htm",
                  "http://vneconomy.vn/timeline/6/trang-1.htm",
                  "http://vneconomy.vn/timeline/7/trang-1.htm",
                  "http://vneconomy.vn/timeline/5/trang-1.htm",
                  "http://vneconomy.vn/timeline/17/trang-1.htm",
                  "http://vneconomy.vn/timeline/19/trang-1.htm",
                  "http://vneconomy.vn/timeline/99/trang-1.htm",
                  "http://vneconomy.vn/timeline/9920/trang-2.htm",
                  "http://vneconomy.vn/timeline/6/trang-2.htm",
                  "http://vneconomy.vn/timeline/7/trang-2.htm",
                  "http://vneconomy.vn/timeline/5/trang-2.htm",
                  "http://vneconomy.vn/timeline/17/trang-2.htm",
                  "http://vneconomy.vn/timeline/19/trang-2.htm",
                  "http://vneconomy.vn/timeline/99/trang-2.htm",
                  "http://vneconomy.vn/timeline/9920/trang-3.htm",
                  "http://vneconomy.vn/timeline/6/trang-3.htm",
                  "http://vneconomy.vn/timeline/7/trang-3.htm",
                  "http://vneconomy.vn/timeline/5/trang-3.htm",
                  "http://vneconomy.vn/timeline/17/trang-3.htm",
                  "http://vneconomy.vn/timeline/19/trang-3.htm",
                  "http://vneconomy.vn/timeline/99/trang-4.htm",
                  "http://vneconomy.vn/timeline/9920/trang-4.htm",
                  "http://vneconomy.vn/timeline/6/trang-4.htm",
                  "http://vneconomy.vn/timeline/7/trang-4.htm",
                  "http://vneconomy.vn/timeline/5/trang-4.htm",
                  "http://vneconomy.vn/timeline/17/trang-4.htm",
                  "http://vneconomy.vn/timeline/19/trang-4.htm",
                  "http://vneconomy.vn/timeline/99/trang-4.htm",
                  "http://vneconomy.vn/timeline/9920/trang-5.htm",
                  "http://vneconomy.vn/timeline/6/trang-5.htm",
                  "http://vneconomy.vn/timeline/7/trang-5.htm",
                  "http://vneconomy.vn/timeline/5/trang-5.htm",
                  "http://vneconomy.vn/timeline/17/trang-5.htm",
                  "http://vneconomy.vn/timeline/19/trang-5.htm",
                  "http://vneconomy.vn/timeline/99/trang-5.htm"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/vneconomy.csv",
    }
    if keyword:
        custom_settings["FEED_URI"] = "data/vneconomy_[" + no_accent_vietnamese(keyword) + "].csv"

    def parse(self, response):
        article_list_xpath = "//li"
        article_list = response.selector.xpath(article_list_xpath)
        for article_short in article_list:
            article_link = self.target_root + article_short.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article_short.xpath(self.article_title_xpath).extract_first().strip(),
                              "time": article_short.xpath(self.time_xpath).extract_first().strip(),
                              "init": article_short.xpath(self.init_xpath).extract_first().strip(),
                              "link": article_link}
            if self.keyword:
                yield Request(url=article_link, callback=self.examine_article,
                              meta={"article_detail": article_detail,
                                    "keyword": self.keyword})
            else:
                yield article_detail

    @staticmethod
    def examine_article(response):
        article_content_xpath = "//div[@class='contentdetail']/p"
        article_content = response.selector.xpath(article_content_xpath)
        for paragraph in article_content:
            keyword = str(response.meta.get("keyword"))
            paragraph_content = str(paragraph.xpath("./text()").extract_first())
            if paragraph_content.find(keyword) != -1:
                article_detail = response.meta.get("article_detail")
                article_detail["paraContainKeyword"] = paragraph_content
                yield article_detail
                break
        pass
