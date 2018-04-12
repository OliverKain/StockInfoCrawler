# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from collections import OrderedDict


class BasicIndexesItem(OrderedDict):
    stock_id = scrapy.Field()
    last_close = scrapy.Field()
    book_value = scrapy.Field()
    highest_52w = scrapy.Field()
    lowest_52w = scrapy.Field()
    pe = scrapy.Field()
    eps = scrapy.Field()
    roa = scrapy.Field()
    roe = scrapy.Field()
    beta = scrapy.Field()
    avg_vol_13w = scrapy.Field()
    on_bal_vol_ratio = scrapy.Field()
    volume = scrapy.Field()
    cap_market = scrapy.Field()
    pass

class BasicIndexesPowerItem(OrderedDict):
    stock_id = scrapy.Field()
    eps = scrapy.Field()
    pe = scrapy.Field()
    roa = scrapy.Field()
    roe = scrapy.Field()
    best_effective = scrapy.Field()
    p_on_b = scrapy.Field()
    stock_at_btm = scrapy.Field()
    debt_ratio = scrapy.Field()
    best_value = scrapy.Field()
    beta = scrapy.Field()
    on_bal_vol_ratio = scrapy.Field()
    best_surf = scrapy.Field()
    avg_strength = scrapy.Field()
    pass

class EventDetailItem(OrderedDict):
    stock_id = scrapy.Field()
    event_type = scrapy.Field()
    exec_date = scrapy.Field()
    diviends = scrapy.Field()
    note = scrapy.Field()
    pass
