# -*- coding: utf-8 -*-

import re


def no_accent_vietnamese(s):
    s = re.sub("[àáạảãâầấậẩẫăằắặẳẵ]", 'a', s)
    s = re.sub("[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", 'A', s)
    s = re.sub("[èéẹẻẽêềếệểễ]", 'e', s)
    s = re.sub("[ÈÉẸẺẼÊỀẾỆỂỄ]", 'E', s)
    s = re.sub("[òóọỏõôồốộổỗơờớợởỡ]", 'o', s)
    s = re.sub("[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", 'O', s)
    s = re.sub("[ìíịỉĩ]", 'i', s)
    s = re.sub("[ÌÍỊỈĨ]", 'I', s)
    s = re.sub("[ùúụủũưừứựửữ]", 'u', s)
    s = re.sub("[ƯỪỨỰỬỮÙÚỤỦŨ]", 'U', s)
    s = re.sub("[ỳýỵỷỹ]", 'y', s)
    s = re.sub("[ỲÝỴỶỸ]", 'Y', s)
    s = re.sub("[Đ]", 'D', s)
    s = re.sub("[đ]", 'd', s)
    # s = re.sub(' ', '_', s)
    return s
