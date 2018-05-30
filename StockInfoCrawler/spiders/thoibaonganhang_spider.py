# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import is_in_filtered_time


class ThoiBaoNganHangSpider(scrapy.Spider):
    name = "thoibaonganhang-spider"

    # Crawling Info
    max_page_depth = 5
    target_root = "http://thoibaonganhang.vn"
    list_xpath = "//div[@class='col_category magin_203 clearfix']/div[@class='list_news clearfix']"
    article_title_xpath = "./div[@class='list_news_title clearfix']/h2/a/text()"
    article_time_xpath = "./div[@class='list_news_decs clearfix']/i/span[2]/text()"
    article_init_xpath = "./div[@class='list_news_decs clearfix']/p/text()"
    article_link_xpath = "./div[@class='list_news_title clearfix']/h2/a/@href"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/su-kien&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/tai-chinh-tien-te&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/bat-dong-san&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/chung-khoan&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/doanh-nghiep-doanh-nhan&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/thi-truong&BRSR={1}".format(target_root, (s-1)*16))
        start_urls.append("{0}/quoc-te&BRSR={1}".format(target_root, (s-1)*16))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/thoibaonganhang.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/thoibaonganhang_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get articles
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.article_link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.article_title_xpath).extract_first().strip(),
                              "time": get_time(article.xpath(self.article_time_xpath).extract_first().strip()),
                              "intro": article.xpath(self.article_init_xpath).extract_first().strip(),
                              "link": article_link
                              }
            if is_in_filtered_time(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                  meta={"article_detail": article_detail, "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@class='entry-content clearfix']//p"
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


def get_time(timestamp_str):
    return timestamp_str[6:10] + "/" + timestamp_str[3:5] + "/" + timestamp_str[0:2]
