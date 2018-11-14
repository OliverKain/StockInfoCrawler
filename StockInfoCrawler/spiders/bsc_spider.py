# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from datetime import date, timedelta


class BscSpider(scrapy.Spider):
    name = "bsc-spider"

    # Crawling Info
    today = date.today().strftime("%Y.%m.%d")
    last_week_str = (date.today() - timedelta(days=7)).strftime("%Y.%m.%d")
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/bsc.csv",
        "DNS_TIMEOUT": "10",
        "DOWNLOAD_DELAY": "1",
    }

    def __init__(self, mode, **kwargs):
        self.mode = mode
        if self.mode == "c":
            company_init_url = "https://www.bsc.com.vn/api/Data/Report/SearchReports" \
                               + "?categoryID=1&sourceID=5&sectorID=null&symbol=&keywords=" \
                               + "&startDate={0}&endDate={1}&startIndex=0&count=500"
            self.start_urls.append(company_init_url.format(self.last_week_str, self.today))
        else:
            market_init_url1 = "https://www.bsc.com.vn/api/Data/Report/SearchReports" \
                               + "?categoryID=4&sourceID=5&sectorID=null&symbol=&keywords=" \
                               + "&startDate={0}&endDate={1}&startIndex=0&count=500"
            self.start_urls.append(market_init_url1.format(self.last_week_str, self.today))
            market_init_url2 = "https://www.bsc.com.vn/api/Data/Report/SearchReports" \
                               + "?categoryID=19&sourceID=5&sectorID=null&symbol=&keywords=" \
                               + "&startDate={0}&endDate={1}&startIndex=0&count=500"
            self.start_urls.append(market_init_url2.format(self.last_week_str, self.today))
        super().__init__(**kwargs)

    def parse(self, response):
        response.selector.remove_namespaces()
        article_list = response.xpath("//ReportInfo")
        for article in article_list:
            init_res = HtmlResponse(
                url="my HTML string",
                body=article.xpath("./Description/text()").extract_first(),
                encoding='utf-8')
            article_detail = {"title": article.xpath("./Title/text()").extract_first().strip(),
                              "time": article.xpath("./Date/text()").extract_first().strip()[:10].replace("-", "/"),
                              "init": "".join(init_res.xpath("//p//text()").extract()).strip(),
                              "link": article.xpath("./LinkDownload/text()").extract_first().strip()}
            yield article_detail
