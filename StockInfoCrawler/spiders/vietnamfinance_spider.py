# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class VietnamFinanceSpider(scrapy.Spider):
    name = "vietnamfinance-spider"

    # Crawling Info
    target_root = "http://vietnamfinance.vn"
    top_focus_xpath = "//div[@class='focus-item']"
    top_focus_title_xpath = "./h2/a/text()"
    top_focus_link_xpath = "./h2/a/@href"
    top_list_xpath = "//div[@class='normal-list-item']/div[@class='normal-item']/div"
    top_list_item_title_xpath = "./h2/a/text()"
    top_list_item_link_xpath = "./h2/a/@href"
    list_xpath = "//div[@class='block-timeline']/div"
    article_title_xpath = "./div/h3/a/text()"
    article_link_xpath = "./div/h3/a/@href"

    start_urls = [
        "http://vietnamfinance.vn/tai-chinh-p1.htm",
        "http://vietnamfinance.vn/tai-chinh-p2.htm",
        "http://vietnamfinance.vn/tai-chinh-p3.htm",
        "http://vietnamfinance.vn/tai-chinh-p4.htm",
        "http://vietnamfinance.vn/ngan-hang-p1.htm",
        "http://vietnamfinance.vn/ngan-hang-p2.htm",
        "http://vietnamfinance.vn/ngan-hang-p3.htm",
        "http://vietnamfinance.vn/ngan-hang-p4.htm",
        "http://vietnamfinance.vn/thi-truong-p1.htm",
        "http://vietnamfinance.vn/thi-truong-p2.htm",
        "http://vietnamfinance.vn/thi-truong-p3.htm",
        "http://vietnamfinance.vn/thi-truong-p4.htm",
        "http://vietnamfinance.vn/do-thi-p1.htm",
        "http://vietnamfinance.vn/do-thi-p2.htm",
        "http://vietnamfinance.vn/do-thi-p3.htm",
        "http://vietnamfinance.vn/do-thi-p4.htm",
        "http://vietnamfinance.vn/tai-chinh-quoc-te-p1.htm",
        "http://vietnamfinance.vn/tai-chinh-quoc-te-p2.htm",
        "http://vietnamfinance.vn/tai-chinh-quoc-te-p3.htm",
        "http://vietnamfinance.vn/tai-chinh-quoc-te-p4.htm",
        "http://vietnamfinance.vn/ma-p1.htm",
        "http://vietnamfinance.vn/ma-p2.htm",
        "http://vietnamfinance.vn/ma-p3.htm",
        "http://vietnamfinance.vn/ma-p4.htm",
        "http://vietnamfinance.vn/startup-p1.htm",
        "http://vietnamfinance.vn/startup-p2.htm",
        "http://vietnamfinance.vn/startup-p3.htm",
        "http://vietnamfinance.vn/startup-p4.htm",
        "http://vietnamfinance.vn/nhan-vat-p1.htm",
        "http://vietnamfinance.vn/nhan-vat-p2.htm",
        "http://vietnamfinance.vn/nhan-vat-p3.htm",
        "http://vietnamfinance.vn/nhan-vat-p4.htm",
        "http://vietnamfinance.vn/thue-p1.htm",
        "http://vietnamfinance.vn/thue-p2.htm",
        "http://vietnamfinance.vn/thue-p3.htm",
        "http://vietnamfinance.vn/thue-p4.htm",
        "http://vietnamfinance.vn/tai-chinh-tieu-dung-p1.htm",
        "http://vietnamfinance.vn/tai-chinh-tieu-dung-p2.htm",
        "http://vietnamfinance.vn/tai-chinh-tieu-dung-p3.htm",
        "http://vietnamfinance.vn/tai-chinh-tieu-dung-p4.htm",
        "http://vietnamfinance.vn/dien-dan-vnf-p1.htm",
        "http://vietnamfinance.vn/dien-dan-vnf-p2.htm",
        "http://vietnamfinance.vn/dien-dan-vnf-p3.htm",
        "http://vietnamfinance.vn/dien-dan-vnf-p4.htm",
    ]
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/vietnamfinance.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/vietnamfinance_refined.csv"
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
            if self.keyword:
                yield Request(url=top_link, callback=self.examine_article,
                               meta={"article_detail": article_detail,
                                     "keyword": self.keyword})
            else:
                yield article_detail
            top_list = response.selector.xpath(self.top_list_xpath)
            for item in top_list:
                item_link = item.xpath(self.top_list_item_link_xpath).extract_first().strip()
                article_detail = {"title": item.xpath(self.top_list_item_title_xpath).extract_first().strip(),
                                  "time": get_time_from_link(item_link),
                                  "intro": "",
                                  "link": self.target_root + item_link
                                  }
                if self.keyword:
                    yield Request(url=item_link, callback=self.examine_article,
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
                              "intro": "",
                              "link": self.target_root + article_link
                              }
            if self.keyword:
                yield Request(url=article_link, callback=self.examine_article,
                               meta={"article_detail": article_detail,
                                     "keyword": self.keyword})
            else:
                yield article_detail

    @staticmethod
    def examine_article(response):
        keyword_list = response.meta.get("keyword")
        article_content_xpath = "//div[@class='news-body-content']/p"
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


def get_time_from_link(link):
    timestamp_str = link[link.rfind("-") + 1:len(link) - len(".htm")]
    return timestamp_str[0:4] + "/" + timestamp_str[4:6] + "/" + timestamp_str[6:8]
