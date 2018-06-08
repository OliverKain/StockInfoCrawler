# -*- coding: utf-8 -*-
import scrapy
from datetime import date, timedelta


class VcscSpider(scrapy.Spider):
    name = "vcsc-spider"

    # Crawling Info
    max_depth = 5
    today = date.today().strftime("%d.%m.%Y").replace(".", "%2F")
    last_week_str = (date.today() - timedelta(days=7)).strftime("%d.%m.%Y").replace(".", "%2F")
    list_xpath = "//div[@class='row news-summary']"
    title_xpath = "./div/div[1]/div/h2/a/text()"
    time_xpath = "./div/div[1]/div/p[@class='date-title']/text()"
    init_xpath = "./div/div[1]/div/p[@class='news-text hidden-sm']/text()"
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/vcsc.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, mode, **kwargs):
        self.mode = mode
        if self.mode == "c":
            for s in range(0, self.max_depth + 1):
                self.start_urls.append(
                    "https://www.vcsc.com.vn/readingbook/loadmore.do"
                    + "?cat=&language=1&from={0}&to={1}&offset={2}&stockcode=&industry="
                    .format(self.last_week_str, self.today, s))
        else:
            for s in range(0, self.max_depth + 1):
                self.start_urls.append(
                    "https://www.vcsc.com.vn/readingbook/loadmore.do"
                    + "?cat=MC&language=1&from={0}&to={1}&offset={2}&stockcode=&industry="
                    .format(self.last_week_str, self.today, s))
        super().__init__(**kwargs)
    
    def parse(self, response):
        article_list = response.xpath(self.list_xpath)
        for article in article_list:
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                              "init": article.xpath(self.init_xpath).extract_first().strip(),
                              "link": response.request.url}
            yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
