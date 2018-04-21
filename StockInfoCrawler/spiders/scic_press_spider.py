# -*- coding: utf-8 -*-
import scrapy


class ScicPressSpider(scrapy.Spider):
    name = "scic-press-spider"

    # Crawling Info
    list_xpath = "//div[@id='content-3columns']/section/div[2]/form/table//tr"
    title_xpath = "./td/a/text()"

    start_urls = ["http://www.scic.vn/index.php/thong-tin-bao-chi.html"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/scic_press.csv",
    }

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip()}
            yield article_detail
