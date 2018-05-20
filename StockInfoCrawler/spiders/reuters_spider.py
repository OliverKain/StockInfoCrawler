# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.http import Request
from commons.is_within_two_weeks import is_within_two_weeks


class ReutersSpider(scrapy.Spider):
    name = "reuters-spider"
    # Crawling Info
    max_page_depth = 100
    target_root = "https://www.reuters.com"
    list_xpath = "//div[@class='news-headline-list  ']/article[@class='story ']"
    title_xpath = "./div[@class='story-content']/a/h3/text()"
    time_xpath = "./div[@class='story-content']/time/span/text()"
    init_xpath = "./div[@class='story-content']/p/text()"
    link_xpath = "./div[@class='story-content']/a/@href"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/news/archive/marketsNews?view=page&page={1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/reuters.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/reuters_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                              "init": article.xpath(self.init_xpath).extract_first().strip().replace('\n', ' '),
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
        article_content_xpath = ""
        if response.selector.xpath("//div[@class='body_1gnLA']/p") is not None:
            article_content_xpath = "//div[@class='body_1gnLA']/p"
        elif response.selector.xpath("//div[@class='body_1gnLA']/div/pre") is not None:
            article_content_xpath = "//div[@class='body_1gnLA']/div/pre"
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


def get_time(time_str):
    if time_str.find("EDT") != -1:
        return datetime.now().strftime("%Y/%m/%d")
    return datetime.strptime(time_str, '%b %d %Y').strftime("%Y/%m/%d")
