# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_within_two_weeks import is_within_two_weeks


class VnEconomySpider(scrapy.Spider):
    name = "vneconomy-spider"

    # Crawling Info
    max_page_depth = 7
    target_root = "http://vneconomy.vn"
    article_title_xpath = "./div/h3/a/text()"
    time_xpath = "./div//span[@class='infonews-time']/text()"
    init_xpath = "./div//p/text()"
    link_xpath = "./div/h3/a/@href"

    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/timeline/5/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/6/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/7/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/17/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/19/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/99/trang-{1}.htm".format(target_root, s))
        start_urls.append("{0}/timeline/9920/trang-{1}.htm".format(target_root, s))

    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/vneconomy.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/vneconomy_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        article_list_xpath = "//li"
        article_list = response.selector.xpath(article_list_xpath)
        for article_short in article_list:
            article_link = self.target_root + article_short.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article_short.xpath(self.article_title_xpath).extract_first().strip(),
                              "time": get_time(article_short.xpath(self.time_xpath).extract_first().strip()),
                              "init": article_short.xpath(self.init_xpath).extract_first().strip(),
                              "link": article_link}
            if is_within_two_weeks(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                  meta={"article_detail": article_detail,
                                        "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@class='contentdetail']/p"
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
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
