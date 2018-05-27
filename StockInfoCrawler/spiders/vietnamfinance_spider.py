# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from commons.is_within_two_weeks import is_within_two_weeks


class VietnamFinanceSpider(scrapy.Spider):
    name = "vietnamfinance-spider"

    # Crawling Info
    max_page_depth = 4
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

    start_urls = []
    for s in range(1, max_page_depth + 1):
        start_urls.append("{0}/tai-chinh-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/ngan-hang-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/thi-truong-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/do-thi-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/tai-chinh-quoc-te-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/ma-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/startup-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/nhan-vat-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/thue-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/tai-chinh-tieu-dung-p{1}.htm".format(target_root, s))
        start_urls.append("{0}/dien-dan-vnf-p{1}.htm".format(target_root, s))

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
                              "time": "",
                              "intro": "",
                              "link": top_link}
            yield Request(url=top_link, callback=self.examine_article,
                           meta={"article_detail": article_detail,
                                 "keyword": self.keyword})
            top_list = response.selector.xpath(self.top_list_xpath)
            for item in top_list:
                item_link = item.xpath(self.top_list_item_link_xpath).extract_first().strip()
                article_detail = {"title": item.xpath(self.top_list_item_title_xpath).extract_first().strip(),
                                  "time": "",
                                  "intro": "",
                                  "link": item_link}
                yield Request(url=item_link, callback=self.examine_article,
                               meta={"article_detail": article_detail,
                                     "keyword": self.keyword})
        # Get articles
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.article_link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.article_title_xpath).extract_first().strip(),
                              "time": "",
                              "intro": "",
                              "link": article_link
                              }
            yield Request(url=article_link, callback=self.examine_article,
                          meta={"article_detail": article_detail,
                                "keyword": self.keyword})

    @staticmethod
    def examine_article(response):
        article_detail = response.meta.get("article_detail")
        keyword_list = response.meta.get("keyword")

        article_content_xpath = "//div[@class='news-body-content']/p"
        article_content = response.selector.xpath(article_content_xpath)

        time_str = "".join(response.selector.xpath("//div[@class='news-author-info']//text()").extract()).strip()
        time_regex = "((0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d\d\d)"
        article_detail["time"] = get_time(re.search(time_regex, time_str).group(1))

        match_flg = False
        if is_within_two_weeks(article_detail.get("time")):
            if keyword_list:
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
            else:
                yield response.meta.get("article_detail")


def get_time(time_str):
    return time_str[6:10] + "/" + time_str[3:5] + "/" + time_str[0:2]
