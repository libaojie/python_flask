#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 装饰器
@Time       : 2018/7/20 16:23
@Author     : libaojie
@File       : decorator.py
@Software   : PyCharm
"""

import traceback
from datetime import datetime
from threading import Thread

from project.app.plugins.log_tool import LogTool
from project.app.plugins.util_tool import UtilTool


def response_json(func):
    def wrapper(*args, **kwargs):
        _ret = func(*args, **kwargs)

        return _ret

    return wrapper


def paginate(func):
    def wrapper(*args, **kwargs):
        LogTool.info("执行分页封装")
        _ret, _val = func(*args, **kwargs)
        if _ret:
            return UtilTool.get_post_json(0, data={'total': _val[1], 'items': _val[0]})
        else:
            return _val

    return wrapper


def log_fun(func):
    """
    获取执行函数名
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        LogTool.print('开始函数：【{0}】'.format(func.__name__))
        _stime = datetime.now()
        _ret = func(*args, **kwargs)
        _etime = datetime.now()
        LogTool.print('结束函数：【{0}】, 执行时间：【{1}】'.format(func.__name__, _etime - _stime))
        return _ret

    return wrapper


def except_fun(func):
    """
    获取函数异常
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        LogTool.print(f'测试函数异常：【{func.__name__}】')
        try:
            _ret = func(*args, **kwargs)
        except Exception as err:
            LogTool.error(traceback.format_exc())
        LogTool.print(f'测试函数异常：【{func.__name__}】')
        return _ret

    return wrapper


def async(f):
    """
    异步多线程
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
