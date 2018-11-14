# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import Request
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
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/bvsc.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, mode, **kwargs):
        self.mode = mode
        if self.mode == "c":
            for s in range(1, self.max_depth + 1):
                self.start_urls.append(
                    ("http://www.bvsc.com.vn/ViewReports.aspx?CategoryID=17&StartDate={0}&EndDate={1}"
                     + "&Cart_ctl00_webPartManager_wp484641337_wp148882691_cbReports_Callback_Param={2}")
                    .format(self.last_week_str, self.today, (s - 1) * 20))
        else:
            for s in range(1, self.max_depth + 1):
                self.start_urls.append(
                    ("http://www.bvsc.com.vn/ViewReports.aspx?CategoryID=33&StartDate={0}&EndDate={1}"
                     + "&Cart_ctl00_webPartManager_wp484641337_wp148882691_cbReports_Callback_Param={2}")
                    .format(self.last_week_str, self.today, (s - 1) * 20))
        super().__init__(**kwargs)

    def parse(self, response):
        response.selector.remove_namespaces()
        res_html = HtmlResponse(url="my HTML string",
                                body=response.selector.xpath("//CallbackContent/text()").extract_first().strip(),
                                encoding='utf-8')
        article_list = res_html.xpath(self.list_xpath)
        for article in article_list:
            time_str = get_time(article.xpath(self.time_xpath).extract_first().strip())
            if is_in_filtered_time(time_str):
                article_link = article.xpath(self.link_xpath).extract_first().strip()
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": time_str,
                                  "init": "",
                                  "link": article_link}
                yield Request(url=article_link, callback=self.get_summary, meta={"article_detail": article_detail})

    @staticmethod
    def get_summary(response):
        # Get article detail from request
        article_detail = response.meta.get("article_detail")
        # Get summary
        summary_xpath = response.selector.xpath("//td[@class='report_row_last']")[4]
        for paragraph_xpath in summary_xpath.xpath("./p"):
            # Append paragraphs
            paragraph = "".join(paragraph_xpath.xpath(".//text()").extract()).strip()
            article_detail["init"] += paragraph + "\r\n"
        yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
