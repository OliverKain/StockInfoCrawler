# -*- coding: utf-8 -*-
import scrapy


class ScicPortfolioSpider(scrapy.Spider):
    name = "scic-portfolio-spider"

    # Crawling Info
    list_xpath = "//div[@id='content-3columns']/section/div[2]/form/table//tr"
    title_xpath = "./td[1]/a/text()"
    time_xpath = "./td[2]/text()"

    start_urls = ["http://www.scic.vn/index.php/investment.html"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/scic_portfolio.csv",
    }

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": article.xpath(self.time_xpath).extract_first().strip()}
            yield article_detail
