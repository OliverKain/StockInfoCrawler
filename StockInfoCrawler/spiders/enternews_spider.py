# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re

from datetime import date
from commons.is_in_filtered_time import is_in_filtered_time


class EnterNewsSpider(scrapy.Spider):
    name = "enternews-spider"
    # Crawling Info
    max_page_depth = 8
    target_root = "http://enternews.vn"
    top_item_xpath = "//div[@class='col-xs-8 auto-padding-right top-center']/div"
    top_item_title_xpath = "./div/div/h1/a/text()"
    top_item_init_xpath = "./p/text()"
    top_item_link_xpath = "./div/div/h1/a/@href"
    top_list_xpath = "//div[@id='top-news-scroll']/ul[@class='list-text']/li"
    top_list_item_title_xpath = "./div[@class='post-info']/a[@class='font-16']/strong/text()"
    top_list_item_link_xpath = "./div[@class='post-info']/a[@class='font-16']/@href"
    list_xpath = "//ul[@class='feed']/li"
    list_item_title_xpath = "./h2/a/text()"
    list_item_time_xpath = "./p[@class='timer mt-5']//text()"
    list_item_init_xpath = "./p[@class='mt-5 mb-15']/text()"
    list_item_link_xpath = "./h2/a/@href"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/dau-tu-c2/page-{1}.html".format(target_root, s))
        start_urls.append("{0}/doanh-nghiep-doanh-nhan-c11/page-{1}.html".format(target_root, s))
        start_urls.append("{0}/tai-chinh-ngan-hang-c7/page-{1}.html".format(target_root, s))
        start_urls.append("{0}/tam-diem-c114/page-{1}.html".format(target_root, s))
    for s in range(1, 20 + 1):
        start_urls.append("{0}/thoi-su-c82/page-{1}.html".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/enternews.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/enternews_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        if str(response.request.url).endswith("page-1.html"):
            # Get top item
            top_item = response.selector.xpath(self.top_item_xpath)
            top_item_link = top_item.xpath(self.top_item_link_xpath).extract_first().strip()
            article_detail = {"title": top_item.xpath(self.top_item_title_xpath).extract_first().strip(),
                              "time": date.today().strftime("%Y/%m/%d"),
                              "init": "",
                              "link": top_item_link}
            if self.keyword:
                yield Request(url=top_item_link, callback=self.examine_article,
                              meta={"article_detail": article_detail,
                                    "keyword": self.keyword})
            else:
                yield article_detail
            # Get top list
            top_list = response.selector.xpath(self.top_list_xpath)
            for item in top_list:
                top_list_item_link = item.xpath(self.top_list_item_link_xpath).extract_first().strip()
                article_detail = {"title": item.xpath(self.top_list_item_title_xpath).extract_first().strip(),
                                  "time": date.today().strftime("%Y/%m/%d"),
                                  "init": "",
                                  "link": top_list_item_link}
            if self.keyword:
                yield Request(url=top_list_item_link, callback=self.examine_article,
                              meta={"article_detail": article_detail,
                                    "keyword": self.keyword})
            else:
                yield article_detail

        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.list_item_link_xpath).extract_first().strip()
            time_str = "".join(article.xpath(self.list_item_time_xpath).extract()).strip()
            time_regex = "((0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d\d\d)"
            time_str = re.search(time_regex,time_str).group(1)
            article_detail = {"title": article.xpath(self.list_item_title_xpath).extract_first().strip(),
                              "time": get_time(time_str),
                              "init": article.xpath(self.list_item_init_xpath).extract_first().strip(),
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
        article_content_xpath = "//article[@id='detail-content']/div[@class='post-content ']/p"
        article_init_xpath = "//article[@id='detail-content']/div[2]/h2/strong/text()"
        article_detail = response.meta.get("article_detail")
        article_detail["init"] = response.selector.xpath(article_init_xpath).extract_first().strip()

        keyword_list = response.meta.get("keyword")
        match_flg = True
        article_content = response.selector.xpath(article_content_xpath)
        
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
            time_xpath = "//div[@class='pull-right mt-5 mr-10']/text()"
            time_str = response.selector.xpath(time_xpath)
            formatted_time = get_time("".join(time_str.extract()).strip())
            article_detail["time"] = formatted_time
            if is_in_filtered_time(formatted_time):
                yield article_detail
                pass


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
