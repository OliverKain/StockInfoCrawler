# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from commons.is_in_filtered_time import get_formatted_past_date


class BaoCongThuongSpider(scrapy.Spider):
    name = "baocongthuong-spider"
    # Crawling Info
    max_page_depth = 3
    article_per_page = 10
    target_root = "http://baocongthuong.com.vn"
    list_xpath = "//div[@class='bx-category-container fw lt clearfix']/article"
    title_xpath = "./h3/a/text()"
    init_xpath = "./div[@class='article-desc']/text()"
    link_xpath = "./h3/a/@href"
    start_urls = []
    for prev_day in range(0, 8):
        for s in range(0, max_page_depth):
            start_urls.append("{0}/thuong-mai&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
            start_urls.append("{0}/cong-nghiep&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
            start_urls.append("{0}/thi-truong&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
            start_urls.append("{0}/tai-chinh&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
            start_urls.append("{0}/doanh-nghiep-doanh-nhan&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
            start_urls.append("{0}/doanh-nghiep-doanh-nhan&fv={1}&BRSR={2}"
                              .format(target_root, get_formatted_past_date(prev_day, "%Y-%m-%d"), s*article_per_page))
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "data/baocongthuong.csv",
    }

    def __init__(self, kw, **kwargs):
        self.keyword = kw
        if self.keyword:
            self.custom_settings["FEED_URI"] = "data/baocongthuong_refined.csv"
        super().__init__(**kwargs)

    def parse(self, response):
        # Get article in list
        article_list = response.selector.xpath(self.list_xpath)
        for article in article_list:
            article_link = article.xpath(self.link_xpath).extract_first().strip()
            article_detail = {"title": article.xpath(self.title_xpath).extract_first().strip(),
                              "time": get_time(response.url),
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
        article_content_xpath = "//div[@class='__MASTERCMS_CONTENT_BODY clearfix']/p"
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


def get_time(url):
    time_str_start_idx = url.find("&fv=") + 4
    time_str = url[time_str_start_idx:time_str_start_idx + 10]
    return time_str[0:4] + "/" + time_str[5:7] + "/" + time_str[8:10]
