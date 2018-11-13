# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import get_formatted_past_date


class BaoDienTuChinhPhuSpider(scrapy.Spider):
    name = "baodientuchinhphu-spider"

    # Crawling Info
    max_page_depth = 2
    target_root = "http://baodientu.chinhphu.vn"
    story_feature_xpath = "//form[@id='aspnetForm']/div[@class='contents hasshadow subpage clearfix']" \
                          "/div/div[@class='story featured']"
    list_xpath = "//form[@id='aspnetForm']/div[@class='contents hasshadow subpage clearfix']" \
                          "/div/div[@class='zonelisting']/div[@class='story']"
    title_xpath = "./p[@class='title']/a/text()"
    time_xpath = "./p[@class='meta']/span/text()"
    init_xpath = "./p[@class='summary']/text()"
    link_xpath = "./p[@class='title']/a/@href"

    start_urls = []
    for prev_day in range(0, 8):
        for s in range(1, max_page_depth + 1):
            start_urls.append("{0}/Kinh-te/7.vgp?ByDate={1}&trang={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%d-%m-%Y"), s))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/baodientuchinhphu.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/baodientuchinhphu_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get headline article
        if "?ByDate={1}&trang=1".format(self.target_root, get_formatted_past_date(0, "%d-%m-%Y")) in response.url:
            story_feature = response.selector.xpath(self.story_feature_xpath)
            article_link = self.target_root + story_feature.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": story_feature.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(story_feature.xpath(self.time_xpath).extract_first().strip()),
                              "init": story_feature.xpath(self.init_xpath).extract_first().strip(),
                              "link": article_link}
            if self.keyword:
                yield Request(url=article_link, callback=self.examine_article,
                              meta={"article_detail": article_detail,
                                    "keyword": self.keyword})
            else:
                yield article_detail

        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = self.target_root + article.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(article.xpath(self.time_xpath).extract_first().strip()),
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
        article_content_xpath = "//div[@class='article-body cmscontents']/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = str(paragraph.xpath(".//text()").extract_first()).lower()
                match_flg = (" " + kw.lower() + " ") in paragraph_content
                if match_flg:
                    # Keyword found
                    break
            if not match_flg:
                # Article don't have the keyword
                break
        if match_flg:
            # Article contains all of the keywords
            yield response.meta.get("article_detail")
            pass


def get_time(time_str):
    return time_str[13:17] + "/" + time_str[10:12] + "/" + time_str[7:9]
