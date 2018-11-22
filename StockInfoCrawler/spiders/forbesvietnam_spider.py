# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import is_in_filtered_time


class ForbesVietNamSpider(scrapy.Spider):
    name = "forbesvietnam-spider"
    # Crawling Info
    max_depth = 10
    target_root = "http://forbesvietnam.com.vn"
    list_xpath = "//div[@class='box-tt-1row']"
    title_xpath = "./div/a/h4/text()"
    time_xpath = "./div/div/ul/li[2]/a/span/text()"
    init_xpath = ""
    link_xpath = "./div/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("{0}/ajax/zone.aspx?zoneid=1&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=6&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=7&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=35&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=13&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=15&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=51&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=52&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=36&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=11&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=12&page={1}".format(target_root, s))
        start_urls.append("{0}/ajax/zone.aspx?zoneid=34&page={1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/forbesvietnam.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/forbesvietnam_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        if article_list is not None:
            for article in article_list:
                article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                                  "init": "",
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
        article_content_xpath = "//div[@id='wrap-detail']/p"
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
            article_detail = response.meta.get("article_detail")
            init_xpath = "//div[@class='sapo_detail cms-desc']/strong//text()"
            article_detail["init"] = str(response.selector.xpath(init_xpath).extract_first())
            yield article_detail
            pass


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
