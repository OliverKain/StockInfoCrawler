# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_within_two_weeks import is_within_two_weeks


class TheLeaderSpider(scrapy.Spider):
    name = "theleader-spider"

    # Crawling Info
    target_root = "http://theleader.vn"
    top_focus_xpath = "//div[@class='block-focus']"
    top_focus_title_xpath = "./h2/a/text()"
    top_focus_link_xpath = "./h2/a/@href"
    top_list_xpath = "//div[@class='block-big-focus']/div[@class='block-normal']/div"
    top_list_item_class_xpath = "./@class"
    top_list_item_title_xpath = "./h2/a/text()"
    top_list_item_link_xpath = "./h2/a/@href"
    list_xpath = "//div[@class='block-list-news']/div[@class='block-list-news-item']"
    article_title_xpath = "./div/h4/a/text()"
    article_link_xpath = "./div/h4/a/@href"
    article_intro_xpath = "./div/p/text()"

    start_urls = [
        "http://theleader.vn/leader-talk-p1.htm",
        "http://theleader.vn/leader-talk-p2.htm",
        "http://theleader.vn/leader-talk-p3.htm",
        "http://theleader.vn/leader-talk-p4.htm",
        "http://theleader.vn/tieu-diem-247-p1.htm",
        "http://theleader.vn/tieu-diem-247-p2.htm",
        "http://theleader.vn/tieu-diem-247-p3.htm",
        "http://theleader.vn/tieu-diem-247-p4.htm",
        "http://theleader.vn/thi-truong-p1.htm",
        "http://theleader.vn/thi-truong-p2.htm",
        "http://theleader.vn/thi-truong-p3.htm",
        "http://theleader.vn/thi-truong-p4.htm",
        "http://theleader.vn/tai-chinh-p1.htm",
        "http://theleader.vn/tai-chinh-p2.htm",
        "http://theleader.vn/tai-chinh-p3.htm",
        "http://theleader.vn/tai-chinh-p4.htm",
        "http://theleader.vn/doanh-nghiep-p1.htm",
        "http://theleader.vn/doanh-nghiep-p2.htm",
        "http://theleader.vn/doanh-nghiep-p3.htm",
        "http://theleader.vn/doanh-nghiep-p4.htm",
        "http://theleader.vn/quoc-te-p1.htm",
        "http://theleader.vn/quoc-te-p2.htm",
        "http://theleader.vn/quoc-te-p3.htm",
        "http://theleader.vn/quoc-te-p4.htm",
        "http://theleader.vn/bat-dong-san/toan-canh-thi-truong-p1.htm",
        "http://theleader.vn/bat-dong-san/toan-canh-thi-truong-p2.htm",
        "http://theleader.vn/bat-dong-san/toan-canh-thi-truong-p3.htm",
        "http://theleader.vn/bat-dong-san/toan-canh-thi-truong-p4.htm",
        "http://theleader.vn/bat-dong-san/doanh-nghiep-du-an-p1.htm",
        "http://theleader.vn/bat-dong-san/doanh-nghiep-du-an-p2.htm",
        "http://theleader.vn/bat-dong-san/doanh-nghiep-du-an-p3.htm",
        "http://theleader.vn/bat-dong-san/doanh-nghiep-du-an-p4.htm",
        "http://theleader.vn/bat-dong-san/san-giao-dich-p1.htm",
        "http://theleader.vn/bat-dong-san/cafe-nha-dat-p1.htm",
        "http://theleader.vn/bat-dong-san/cafe-nha-dat-p2.htm",
        "http://theleader.vn/bat-dong-san/cafe-nha-dat-p3.htm",
        "http://theleader.vn/bat-dong-san/cafe-nha-dat-p4.htm",
    ]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/theleader.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/theleader_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get top_focus
        if str(response.request.url).endswith("p1.htm"):
            top_focus = response.selector.xpath(self.top_focus_xpath)
            top_link = top_focus.xpath(self.top_focus_link_xpath).extract_first().strip()
            article_detail = {"title": top_focus.xpath(self.top_focus_title_xpath).extract_first().strip(),
                              "time": get_time_from_link(top_link),
                              "intro": "",
                              "link": self.target_root + top_link}
            if is_within_two_weeks(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=(self.target_root + top_link), callback=self.examine_article,
                                   meta={"article_detail": article_detail,
                                         "keyword": self.keyword})
                else:
                    yield article_detail
            top_list = response.selector.xpath(self.top_list_xpath)
            for item in top_list:
                top_list_item_class = item.xpath(self.top_list_item_class_xpath).extract_first().strip()
                if top_list_item_class == "block-normal-item" or top_list_item_class == "block-normal-item last":
                    item_link = item.xpath(self.top_list_item_link_xpath).extract_first().strip()
                    article_detail = {"title": item.xpath(self.top_list_item_title_xpath).extract_first().strip(),
                                      "time": get_time_from_link(item_link),
                                      "intro": "",
                                      "link": self.target_root + item_link
                                      }
                    if is_within_two_weeks(article_detail.get("time")):
                        if self.keyword:
                            yield Request(url=(self.target_root + item_link), callback=self.examine_article,
                                           meta={"article_detail": article_detail,
                                                 "keyword": self.keyword})
                        else:
                            yield article_detail
        # Get articles
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.article_link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.article_title_xpath).extract_first().strip(),
                              "time": get_time_from_link(article_link),
                              "intro": article.xpath(self.article_intro_xpath).extract_first().strip(),
                              "link": self.target_root + article_link
                              }
            if is_within_two_weeks(article_detail.get("time")):
                if self.keyword:
                    yield Request(url=(self.target_root + article_link), callback=self.examine_article,
                                   meta={"article_detail": article_detail,
                                         "keyword": self.keyword})
                else:
                    yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@class='news-detail-body-wrapper']/p"
        article_content = response.selector.xpath(article_content_xpath)
        match_flg = False
        for kw in keyword_list:
            for paragraph in article_content:
                paragraph_content = str(paragraph.xpath(".//text()").extract_first())
                if paragraph_content.lower().find(" " + kw + " ") != -1:
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


def get_time_from_link(link):
    timestamp_str = link[link.rfind("-") + 1:len(link) - len(".htm")]
    return timestamp_str[0:4] + "/" + timestamp_str[4:6] + "/" + timestamp_str[6:8]
