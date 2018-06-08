# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from datetime import date, timedelta


class MbsSpider(scrapy.Spider):
    name = "mbs-spider"

    # Crawling Info
    max_depth = 5
    target_root = "https://mbs.com.vn"
    today = date.today().strftime("%d-%m-%Y")
    last_week_str = (date.today() - timedelta(days=7)).strftime("%d-%m-%Y")
    list_xpath = "//div[@id='list_content']"
    title_xpath = "./div[@class='it-ct']/div[@class='tit']/a/text()"
    time_xpath = "./div[@class='it-ct']/div[@class='dat']//text()"
    link_xpath = "./div[@class='it-ct']/div[@class='tit']/a/@href"
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/mbs.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, mode, **kwargs):
        self.mode = mode
        if self.mode == "c":
            for s in range(1, self.max_depth + 1):
                company_init_url = \
                        "https://mbs.com.vn/vi/trung-tam-nghien-cuu/bao-cao-phan-tich/nghien-cuu-co-phieu" \
                        + "?page={0}&dateFrom={1}&dateTo={2}&searchText=&parrent=0"
                self.start_urls.append(company_init_url.format(s, self.last_week_str, self.today))
        else:
            for s in range(1, self.max_depth + 1):
                company_init_url = \
                        "https://mbs.com.vn/vi/trung-tam-nghien-cuu/bao-cao-phan-tich/ban-tin-ngay" \
                        + "?page={0}&dateFrom={1}&dateTo={2}&searchText=&parrent=0"
                self.start_urls.append(company_init_url.format(s, self.last_week_str, self.today))
        super().__init__(**kwargs)

    def parse(self, response):
        article_list = response.xpath(self.list_xpath)
        article_list_left = article_list.xpath("./div[@class='item left']")
        for article in article_list_left:
            time_str = get_time("".join(article.xpath(self.time_xpath).extract())[-10:])
            article_detail = {
                "title": article.xpath(self.title_xpath).extract_first().strip(),
                "time": time_str,
                "link": self.target_root + article.xpath(self.link_xpath).extract_first().strip()}
            yield article_detail
        article_list_right = article_list.xpath("./div[@class='item right']")
        for article in article_list_right:
            time_str = get_time("".join(article.xpath(self.time_xpath).extract())[-10:])
            article_detail = {
                "title": article.xpath(self.title_xpath).extract_first().strip(),
                "time": time_str,
                "link": self.target_root + article.xpath(self.link_xpath).extract_first().strip()}
            yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
