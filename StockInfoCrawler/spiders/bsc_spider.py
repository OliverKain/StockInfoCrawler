# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from datetime import date, timedelta


class BscSpider(scrapy.Spider):
    name = "bsc-spider"

    # Crawling Info
    today = date.today().strftime("%Y.%m.%d")
    last_two_weeks_str = (date.today() - timedelta(days=14)).strftime("%Y.%m.%d")
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/bsc.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, **kwargs):
        init_url = "https://www.bsc.com.vn/api/Data/Report/SearchReports" \
                   + "?categoryID=1&sourceID=5&sectorID=null&symbol=&keywords=" \
                   + "&startDate={0}&endDate={1}&startIndex=0&count=500"
        self.start_urls.append(init_url.format(self.last_two_weeks_str, self.today))
        super().__init__(**kwargs)

    def parse(self, response):
        article_list = response.selector.xpath("//ReportInfo")
        for article in article_list:
            article_detail = {"title": article.get("Title"),
                              "time": str(article.get("Date")[:10]).replace("-", "/"),
                              "link": article.get("LinkDownload")}
            yield article_detail