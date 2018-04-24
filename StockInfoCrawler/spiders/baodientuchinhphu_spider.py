# -*- coding: utf-8 -*-
import scrapy


class BaoDienTuChinhPhuSpider(scrapy.Spider):
    name = "baodientuchinhphu-spider"

    # Crawling Info
    target_root = "http://baodientu.chinhphu.vn/"
    story_feature_xpath = "//form[@id='aspnetForm']/div[8]/div/div[@class='story featured']"
    list_xpath = "//form[@id='aspnetForm']/div[8]/div/div[@class='zonelisting']/div[@class='story']"
    title_xpath = "./p[@class='title']/a/text()"
    time_xpath = "./p[@class='meta']/span/text()"
    summary_xpath = "./p[@class='summary']/text()"

    start_urls = ["http://baodientu.chinhphu.vn/Kinh-te/7.vgp"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/baodientuchinhphu.csv",
    }

    def parse(self, response):
        story_feature = response.selector.xpath(self.story_feature_xpath)
        article_detail = {"title": story_feature.xpath(self.title_xpath).extract_first().strip(),
                          "time": story_feature.xpath(self.time_xpath).extract_first().strip(),
                          "summary": story_feature.xpath(self.summary_xpath).extract_first().strip()}
        yield article_detail
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": article.xpath(self.time_xpath).extract_first().strip(),
                              "summary": article.xpath(self.summary_xpath).extract_first().strip()}
            yield article_detail