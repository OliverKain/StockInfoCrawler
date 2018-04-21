# -*- coding: utf-8 -*-
import scrapy


class SbvSpider(scrapy.Spider):
    name = "sbv-spider"

    # Crawling Info
    list_xpath = "//div[@class='x28i']/div[3]/div"
    div_article_id_xpath = "./@id"
    title_xpath = "./a/text()"
    time_xpath = "./span//text()"

    start_urls = ["https://www.sbv.gov.vn/webcenter/portal/vi/menu/rm/apph/tcnh"]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/sbv.csv",
    }

    def parse(self, response):
        article_list = response.selector.xpath(self.list_xpath)
        # Test response, remove later
        # yield {"test": article_list.extract_first()}
        for article in article_list:
            div_article_anchor = "region:i2"
            div_id = str(article.xpath(self.div_article_id_xpath).extract_first()).strip()
            if div_id.find(div_article_anchor) > -1:
                article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                  "time": article.xpath(self.time_xpath).extract_first().strip()
                                      .replace("(", "").replace(")", "")}
                yield article_detail
