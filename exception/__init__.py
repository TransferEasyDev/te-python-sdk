# -*- coding: utf-8 -*-
# @Time : 2022/8/17下午5:42
# @Author : anwen
# @Email : anwen@transfereasy.com
# @FileName : __init__.py.py
# @Software: PyCharm
# -*- coding: utf-8 -*-


class HPException(Exception):

    _error = 'EX_SYSTEM_ERROR'
    _message = 'Server Got An Exception.'
    code = 500
    result_code = None  # 退款错误码

    def __init__(self, *, message=None, code=None):
        if message is not None:
            self._message = message
        if code:
            self.result_code = code

    def __str__(self):
        return f'{self._error} => {self._message}'

    def __repr__(self):
        return self.__str__()

    @property
    def error(self):
        return self._error

    @property
    def message(self):
        return self._message
