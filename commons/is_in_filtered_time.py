# -*- coding: utf-8 -*-
from datetime import date, timedelta


def is_in_filtered_time(time_str):
    last_week_str = (date.today() - timedelta(days=7)).strftime("%Y/%m/%d")
    if time_str >= last_week_str:
        return True
    return False
