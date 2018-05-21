# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from scrapy.http import Request
from datetime import date, timedelta


class HsxSpider(scrapy.Spider):
    # TODO Iterate pages
    name = "hsx-spider"

    # Crawling Info
    target_root = "https://hnx.vn/"
    today = date.today().strftime("%d.%m.%Y")
    last_two_weeks_str = (date.today() - timedelta(days=14)).strftime("%d.%m.%Y")
    start_urls = []
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/hsx.csv",
    }
    list_json_id = "rows"

    def __init__(self, kw, **kwargs):
        init_url = "https://www.hsx.vn/Modules/CMS/Web/ArticleInCategory/dca0933e-a578-4eaf-8b29-beb4575052c5"\
                   + "?exclude=00000000-0000-0000-0000-000000000000&lim=True&pageFieldName1=FromDate"\
                   + "&pageFieldValue1={0}&pageFieldOperator1=eq&pageFieldName2=ToDate"\
                   + "&pageFieldValue2={1}&pageFieldOperator2=eq&pageFieldName3=TokenCode"\
                   + "&pageFieldValue3=&pageFieldOperator3=eq&pageFieldName4=CategoryId"\
                   + "&pageFieldValue4=dca0933e-a578-4eaf-8b29-beb4575052c5"\
                   + "&pageFieldOperator4=eq&pageCriteriaLength=4"\
                   + "&_search=false&nd=1526850145275&rows=30&page={2}&sidx=id&sord=desc"
        list_json_link = init_url.format(self.last_two_weeks_str, self.today, 1)
        response = requests.get(url=list_json_link)
        response_json = json.loads(response.text)
        total_page = response_json.get("total")
        for i in range(total_page + 1):
            self.start_urls.append(init_url.format(self.last_two_weeks_str, self.today, i))
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/hsx_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            article_detail = {"stock_id": article.xpath(self.stock_id_xpath).extract_first().strip(),
                              "title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": article.xpath(self.time_xpath).extract_first().strip()}
            yield article_detail
