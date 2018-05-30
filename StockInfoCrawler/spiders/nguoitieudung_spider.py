# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import is_in_filtered_time


class NguoiTieuDungSpider(scrapy.Spider):
    name = "nguoitieudung-spider"
    # Crawling Info
    max_depth = 10
    target_root = "http://nguoitieudung.com.vn"
    list_xpath = "//div[@class='col583 left']/ul[@class='list-news-cat']/li"
    title_xpath = "./h2/a/text()"
    time_xpath = "./time/span[@class='caption-time']/text()"
    init_xpath = "./p/text()"
    link_xpath = "./h2/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("{0}/thi-truong/p{1}".format(target_root, s))
        start_urls.append("{0}/doanh-nghiep--thuong-hieu/p{1}".format(target_root, s))
        start_urls.append("{0}/doanh-nhan/p{1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/nguoitieudung.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/nguoitieudung_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                              "init": article.xpath(self.init_xpath).extract_first().strip(),
                              "link": article_link}
            if is_in_filtered_time(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                   meta={"article_detail": article_detail,
                                         "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@id='content_detail_news']/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = str(paragraph.xpath(".//text()").extract_first())
                if paragraph_content.lower().find(" " + kw + " ") != -1:
                    # Keyword found
                    match_flg = True
                    break
                # Keyword not found
                match_flg = False
            # Article did not have a keyword
            if not match_flg:
                break
        if match_flg:
            yield response.meta.get("article_detail")
            pass


def get_time(time_str):
    return time_str[13:17] + "/" + time_str[10:12] + "/" + time_str[7:9]
