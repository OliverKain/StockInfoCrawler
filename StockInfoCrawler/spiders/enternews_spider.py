# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import is_in_filtered_time


class EnterNewsSpider(scrapy.Spider):
    name = "enternews-spider"
    # Crawling Info
    max_page_depth = 8
    target_root = "http://http://enternews.vn"
    top_item_xpath = "//div[@class='col-xs-8 auto-padding-right top-center']/div[@class='top_item']"
    top_list_xpath = "//div[@id='top-news-scroll']/ul[@class='list-text']/li"
    list_xpath = "//ul[@class='feed']/li"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/doanh-nghiep-doanh-nhan-c11/page-{1}.html".format(target_root, s))
        start_urls.append("{0}/thuong-mai/thi-truong-trong-nuoc&BRSR={1}".format(target_root, s))
        start_urls.append("{0}/thuong-mai/thi-truong-mien-nui&BRSR={1}".format(target_root, s))
        start_urls.append("{0}/thuong-mai/thuong-mai-dien-tu&BRSR={1}".format(target_root, s))
    for s in range(1, 20 + 1):
        start_urls.append("{0}/thoi-su-c82/page-{1}.html".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/enternews.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/enternews.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get headline article
        if str(response.request.url).endswith("&BRSR=0"):
            headline = response.selector.xpath(self.headline_xpath)
            headline_link = headline.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": headline.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(headline.xpath(self.headline_time_xpath).extract_first().strip()),
                              "init": headline.xpath(self.init_xpath).extract_first().strip(),
                              "link": headline_link}
            if is_in_filtered_time(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=headline_link, callback=self.examine_article,
                                   meta={"article_detail": article_detail,
                                         "keyword": self.keyword})
                else:
                    yield article_detail
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
        article_content_xpath = "//article[@class='__MASTERCMS_CONTENT']/div/p"
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
    return time_str[14:18] + "/" + time_str[11:13] + "/" + time_str[8:10]
