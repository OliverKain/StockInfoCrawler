# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class ThoiBaoTaiChinhVietNamSpider(scrapy.Spider):
    name = "thoibaotaichinhvietnam-spider"
    # Crawling Info
    max_depth = 3
    target_root = "http://thoibaotaichinhvietnam.vn"
    list_xpath = "//div[@class='component_content']/div"
    div_class_xpath = "./@class"
    title_xpath = "./div/div[@class='title']/div[@class='noindex']/a/text()"
    time_xpath = "./div/div[@class='title']/div[@class='noindex']/span/text()"
    init_xpath = "./div/div[@class='introtext']/text()"
    link_xpath = "./div/div[@class='title']/div[@class='noindex']/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("{0}/pages/xa-hoi-51226.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/thoi-su-51316.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/nhip-song-tai-chinh-3.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/thue-voi-cuoc-song-4.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/chung-khoan-5.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/tien-te-bao-hiem-6.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/kinh-doanh-7.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/nhip-cau-tieu-dung-8.aspx?p={1}".format(target_root, s))
        start_urls.append("{0}/pages/quoc-te-51329.aspx?p={1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/thoibaotaichinhvietnam.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/thoibaotaichinhvietnam_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            div_class = str(article.xpath(self.div_class_xpath).extract_first())
            if div_class.find("row") > -1:
                article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                                  "init": article.xpath(self.init_xpath).extract_first().strip(),
                                  "link": article_link}
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                   meta={"article_detail": article_detail,
                                         "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@class='article-content article-content02']/div/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = str(paragraph.xpath(".//text()").extract_first())
                if paragraph_content.find(kw) != -1:
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