# -*- coding: utf-8 -*-
import scrapy
from commons.is_in_filtered_time import is_in_filtered_time


class VcbsSpider(scrapy.Spider):
    name = "vcbs-spider"

    # Crawling Info
    max_depth = 5
    target_root = "http://vcbs.com.vn"
    list_xpath = "//div[@class='content_2col_block_content ']/ul[1]/li"
    title_xpath = "./a/p//text()"
    date_xpath = "./span[@class='nice_date']/p[@class='date']/text()"
    month_year_xpath = "./span[@class='nice_date']/p[@class='month_year']/text()"
    link_xpath = "./a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("http://vcbs.com.vn/vn/Services/AnalysisReports/4?page={0}".format(s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/vcbs.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }
    
    def parse(self, response):
        article_list = response.xpath(self.list_xpath)
        for article in article_list:
            time_str = get_time(article.xpath(self.date_xpath).extract_first().strip()
                                + "." + article.xpath(self.month_year_xpath).extract_first().strip())
            # if is_in_filtered_time(time_str):
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": time_str,
                              "link": self.target_root + article.xpath(self.link_xpath).extract_first().strip()}
            yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
