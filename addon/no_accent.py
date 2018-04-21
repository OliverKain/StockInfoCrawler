# -*- coding: utf-8 -*-

import re


def no_accent_vietnamese(s):
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'èéẹẻẽêềếệểễ', 'e', s)
    s = re.sub(u'ÈÉẸẺẼÊỀẾỆỂỄ', 'E', s)
    s = re.sub(u'òóọỏõôồốộổỗơờớợởỡ', 'o', s)
    s = re.sub(u'ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ', 'O', s)
    s = re.sub(u'ìíịỉĩ', 'i', s)
    s = re.sub(u'ÌÍỊỈĨ', 'I', s)
    s = re.sub(u'ùúụủũưừứựửữ', 'u', s)
    s = re.sub(u'ƯỪỨỰỬỮÙÚỤỦŨ', 'U', s)
    s = re.sub(u'ỳýỵỷỹ', 'y', s)
    s = re.sub(u'ỲÝỴỶỸ', 'Y', s)
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    # s = re.sub(' ', '_', s)
    return s
