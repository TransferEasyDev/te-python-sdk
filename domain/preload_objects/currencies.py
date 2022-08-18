# -*- coding: utf-8 -*-
# 入口 - 常用的所有币种
# 对应了数据库里的配置
# 可以直接import在某个场景使用


def take_currency_by(*, iso_code):
    iso_code = iso_code.upper() if iso_code is not None else None
    if iso_code not in ['CNY', 'HKD', 'USD', 'CAD', 'GBP', 'AUD', 'EUR', 'NZD', 'KRW', 'JPY', 'CNH', 'MOP']:
        return 'No Such Curreny'
    return iso_code




