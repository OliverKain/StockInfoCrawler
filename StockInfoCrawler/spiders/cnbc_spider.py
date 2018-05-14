# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class CnbcSpider(scrapy.Spider):
    name = "cnbc-spider"
    # Crawling Info
    max_depth = 10
    target_root = "https://www.cnbc.com"
    headline_xpath = "//div[@id='feature']/div[1]"
    headline_list_xpath = "//div[@id='filmstrip_feature']/table/tbody/tr/td"
    list_xpath = "//ul[@id='pipeline_assetlist_0']/li"
    title_xpath = ".//div[@class='headline']/a/text()"
    time_xpath = ".//div[@class='headline']/a/@href"
    init_xpath = ".//p[@class='desc']/text()"
    link_xpath = ".//div[@class='headline']/a/@href"
    start_urls = []
    for s in range(1, max_depth + 1):
        start_urls.append("{0}/economy/?page={1}".format(target_root, s))
        start_urls.append("{0}/finance/?page={1}".format(target_root, s))
        start_urls.append("{0}/investing/?page={1}".format(target_root, s))
        start_urls.append("{0}/make-it/money/?page={1}".format(target_root, s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/cnbc.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/cnbc_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Not make-it sub
        if str(response.request.url).find("make-it") == -1:
            # Get headline article
            if str(response.request.url).endswith("?page=1"):
                headline = response.selector.xpath(self.headline_xpath)
                if headline is not None:
                    headline_link = self.target_root + headline.xpath(self.link_xpath).extract_first().strip()
                    if headline_link.find("/video/") == -1:
                        article_detail = {"title": headline.xpath(self.title_xpath).extract_first().strip(),
                                        "time": headline.xpath(self.time_xpath).extract_first().strip()[1:11],
                                        "init": headline.xpath(self.init_xpath).extract_first().strip(),
                                        "link": headline_link}
                        if self.keyword:
                            yield Request(url=headline_link, callback=self.examine_article,
                                        meta={"article_detail": article_detail,
                                                "keyword": self.keyword})
                        else:
                            yield article_detail

            # Get headline article in list
            headline_list = response.selector.xpath(self.headline_list_xpath)
            for headline in headline_list:
                if headline.xpath("./@id").extract_first() is None:
                    headline_link = self.target_root + headline.xpath(self.link_xpath).extract_first().strip()
                    if headline_link.find("/video/") == -1:
                        article_detail = {"title": headline.xpath(self.title_xpath).extract_first().strip(),
                                        "time": headline.xpath(self.time_xpath).extract_first().strip()[1:11],
                                        "init": headline.xpath(self.init_xpath).extract_first().strip(),
                                        "link": headline_link}
                        if self.keyword:
                            yield Request(url=headline_link, callback=self.examine_article,
                                        meta={"article_detail": article_detail,
                                                "keyword": self.keyword})
                        else:
                            yield article_detail

            # Get article in list
            article_list = response.selector.xpath(self.list_xpath)
            for article in article_list:
                if article.xpath("./@id").extract_first() is None:
                    article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
                    if article_link.find("/video/") == -1:
                        article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                        "time": article.xpath(self.time_xpath).extract_first().strip()[1:11],
                                        "init": article.xpath(self.init_xpath).extract_first().strip(),
                                        "link": article_link}
                        if self.keyword:
                            yield Request(url=article_link, callback=self.examine_article,
                                        meta={"article_detail": article_detail,
                                                "keyword": self.keyword})
                        else:
                            yield article_detail

        # Make-it sub
        else:
            # Get headline article
            if str(response.request.url).endswith("?page=1"):
                makeit_headline_xpath = self.list_xpath + "/div/a"
                headline = response.selector.xpath(makeit_headline_xpath)
                if headline is not None:
                    headline_link = self.target_root + headline.xpath("./@href").extract_first().strip()
                    if headline_link.find("/video/") == -1:
                        article_detail = {"title": headline.xpath("./div[@class='headline']/text()").extract_first().strip(),
                                        "time": headline.xpath("./@href").extract_first().strip()[1:11],
                                        "init": headline.xpath(self.init_xpath).extract_first().strip(),
                                        "link": headline_link}
                        if self.keyword:
                            yield Request(url=headline_link, callback=self.examine_article,
                                        meta={"article_detail": article_detail,
                                                "keyword": self.keyword})
                        else:
                            yield article_detail

            # Get article in list
            article_list = response.selector.xpath(self.list_xpath)
            for article in article_list:
                if str(article.xpath("./@class").extract_first()).find(" card") != -1:
                    article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
                    if article_link.find("/video/") == -1:
                        article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                                        "time": article.xpath(self.time_xpath).extract_first().strip()[1:11],
                                        "init": article.xpath(self.init_xpath).extract_first().strip(),
                                        "link": article_link}
                        if self.keyword:
                            yield Request(url=article_link, callback=self.examine_article,
                                        meta={"article_detail": article_detail,
                                                "keyword": self.keyword})
                        else:
                            yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@id='article_body']//div[@class='group']/p"
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
