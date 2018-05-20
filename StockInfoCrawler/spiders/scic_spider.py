# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class ScicSpider(scrapy.Spider):
    name = "scic-spider"

    # Crawling Info
    max_page_depth = 5
    target_root = "http://www.scic.vn"
    list_xpath = "//div[@id='content-3columns']/section/div[2]/form/table//tr"
    title_xpath = "./td[1]/a/text()"
    time_xpath = "./td[2]/text()"
    link_xpath = "./td[1]/a/@href"
    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/index.php/investment.html?start={1}".format(target_root, (s - 1) * 20))
        start_urls.append("{0}/index.php/thong-tin-bao-chi.html?start={1}".format(target_root, (s - 1) * 15))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/scic.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/scic_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        if article_list is not None:
            for article in article_list:
                article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
                if str(response.request.url).find("thong-tin-bao-chi.html") > -1:
                    article_time = ""
                else:
                    article_time = article.xpath(self.time_xpath).extract_first().strip()
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": article_time,
                                  "init": "",
                                  "link": article_link}
                if self.keyword:
                    yield Request(url=article_link, callback=self.examine_article,
                                  meta={"article_detail": article_detail, "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//article[@class='item-page']/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = str(paragraph.xpath(".//text()").extract_first())
                if paragraph_content.find(kw) != -1:
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
            pass
