# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import is_in_filtered_time


class BloombergSpider(scrapy.Spider):
    name = "bloomberg-spider"
    # Crawling Info
    max_depth = 20
    target_root = "http://bloomberg.com"
    list_xpath = "//div[@class='search-result-items']/div"
    title_xpath = "./article/div/h1/a//text()"
    time_xpath = "./article/div/div[@class='search-result-story__metadata']" \
                 "/span[@class='metadata-timestamp']/time/@datetime"
    init_xpath = "./article/div/div[@class='search-result-story__body']//text()"
    link_xpath = "./article/div/h1/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("{0}/search?query=vietnam&page={1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/bloomberg.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/bloomberg_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.link_xpath).extract_first().strip()
            if str(article_link).find("videos") != -1:
                # ignore videos
                continue
            article_detail = {"title": "".join(article.xpath(self.title_xpath).extract()).strip(),
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                              "init": "".join(article.xpath(self.init_xpath).extract()).strip(),
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
        article_content_xpath = "//div[@class='body-copy fence-body']/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = "".join(str(paragraph.xpath(".//text()").extract()))
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
    return str(time_str[:10]).replace("-", "/")
