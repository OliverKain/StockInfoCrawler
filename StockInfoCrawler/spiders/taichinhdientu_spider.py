# -*- coding: utf-8 -*-
import scrapy


class TaiChinhDienTuSpider(scrapy.Spider):
    name = "taichinhdientu-spider"

    # Crawling Info
    target_root = "http://www.taichinhdientu.vn/"
    story_feature_xpath = "//article[@class='story feature']"
    story_feature_title_xpath = ".//h2/a/text()"
    story_feature_summary_xpath = "./div[@class='summary']/div/text()"
    list_xpath = "//div[@class='list-article hzol-clear']/article"
    title_xpath = "./header/h2/a/text()"
    time_xpath = "./header/div[@class='meta']/time/text()"
    summary_xpath = "./header/div[@class='summary']/div/text()"

    start_urls = ["http://www.taichinhdientu.vn/thongke-dubao/",
                  "http://www.taichinhdientu.vn/tai-chinh-247/"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/taichinhdientu.csv",
    }

    def parse(self, response):
        story_feature = response.selector.xpath(self.story_feature_xpath)
        article_detail = {"title": story_feature.xpath(self.story_feature_title_xpath).extract_first().strip(),
                          "time": "",
                          "summary": story_feature.xpath(self.story_feature_summary_xpath).extract_first().strip()}
        yield article_detail
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": article.xpath(self.time_xpath).extract_first().strip(),
                              "summary": article.xpath(self.summary_xpath).extract_first().strip()}
            yield article_detail
