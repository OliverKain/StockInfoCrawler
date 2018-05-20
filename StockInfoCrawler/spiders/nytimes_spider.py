# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request
from commons.is_within_two_weeks import is_within_two_weeks


class NYTimesSpider(scrapy.Spider):
    name = "nytimes-spider"
    # Crawling Info
    max_page_depth = 20
    target_root = "https://www.nytimes.com"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/"
                          + "section/business/dealbook?q=&sort=newest&page={0}".format(s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/nytimes.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/nytimes_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        response_json = json.loads(response.text)
        article_list = response_json["members"]["items"]
        for article in article_list:
            article_link = article["url"]
            article_detail = {"title": article["headline"],
                              "time": get_time(article["created"]),
                              "init": article["summary"],
                              "link": article_link}
            if is_within_two_weeks(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                  meta={"article_detail": article_detail, "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        if str(response.request.url) == "https://www.nytimes.com/2018/05/07/style/warren-buffett-omaha.html":
            print()
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//article[@id='story']//p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = "".join(paragraph.xpath(".//text()").extract())
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


def get_time(time_str):
    return time_str[0:10].replace("-", "/")
