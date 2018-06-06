# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from commons.is_in_filtered_time import is_in_filtered_time


class HnxSpider(scrapy.Spider):
    # TODO Iterate pages
    name = "hnx-spider"

    # Crawling Info
    target_root = "https://hnx.vn/"
    list_xpath = "//div[@id='divContainTable']/table/tbody/tr"
    time_xpath = "./td[2]/text()"
    stock_id_xpath = "./td[3]/a/text()"
    org_name_xpath = "./td[4]/a/text()"
    title_hnx_xpath = "./td[4]/a/text()"
    title_issuer_xpath = "./td[5]/a/text()"

    start_urls = [
        "https://hnx.vn/ModuleArticles/ArticlesCPEtfs/NextPageTinCPNY_CBTCPH"
        + "?pNumPage=1&pAction=0&pNhomTin=&pTieuDeTin=&pMaChungKhoan=&pFromDate=&pToDate=&pOrderBy=&pNumRecord=500",
        "https://hnx.vn/ModuleArticles/ArticlesCPEtfs/NextPageTinCPNY"
        + "?pNumPage=1&pAction=0&pNhomTin=&pTieuDeTin=&pMaChungKhoan=&pFromDate=&pToDate=&pOrderBy=&pNumRecord=500",
    ]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/hnx.csv",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield FormRequest(url, callback=self.parse, formdata=None, method="POST",
                        cookies={
                            "ASP.NET_SessionId": "o4paaccs0rfnrsfwxkp04ja1",
                            "language": "vi-VN"
                        })

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            title = ""
            init = ""
            if response.request.url.find("NextPageTinCPNY_CBTCPH") != -1:
                title = article.xpath(self.stock_id_xpath).extract_first().strip() \
                            + " - " + article.xpath(self.org_name_xpath).extract_first().strip()
                init = article.xpath(self.title_issuer_xpath).extract_first().strip()
            else:
                title = article.xpath(self.stock_id_xpath).extract_first().strip()
                init = article.xpath(self.title_hnx_xpath).extract_first().strip()
            article_detail = {"title": title,
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
                              "init": init,}
            if is_in_filtered_time(article_detail.get("time")):
                yield article_detail


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]