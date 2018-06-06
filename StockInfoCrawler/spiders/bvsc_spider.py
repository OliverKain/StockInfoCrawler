# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from datetime import date, timedelta
from commons.is_in_filtered_time import is_in_filtered_time


class BvscSpider(scrapy.Spider):
    name = "bvsc-spider"

    # Crawling Info
    max_depth = 3
    today = date.today().strftime("%d-%m-%Y")
    last_week_str = (date.today() - timedelta(days=7)).strftime("%d-%m-%Y")
    list_xpath = "//table/tr[@class='report_row']"
    title_xpath = "./td[3]/a/text()"
    time_xpath = "./td[1]/text()"
    link_xpath = "./td[3]/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append(
            ("http://www.bvsc.com.vn/ViewReports.aspx?CategoryID=17&StartDate={0}&EndDate={1}"
             + "&Cart_ctl00_webPartManager_wp484641337_wp148882691_cbReports_Callback_Param={2}")
            .format(last_week_str, today, (s - 1) * 20))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/bvsc.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def parse(self, response):
        response.selector.remove_namespaces()
        res_html = HtmlResponse(url="my HTML string",
                                body=response.selector.xpath("//CallbackContent/text()").extract_first().strip(),
                                encoding='utf-8')
        article_list = res_html.xpath(self.list_xpath)
        for article in article_list:
            time_str = get_time(article.xpath(self.time_xpath).extract_first().strip())
            if is_in_filtered_time(time_str):
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": time_str,
                                  "init": "",
                                  "link": article.xpath(self.link_xpath).extract_first().strip()}
                yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
