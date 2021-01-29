#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/9 10:25
@Author     : libaojie
@File       : time_tool.py
@Software   : PyCharm
"""
import datetime
import time


class TimeTool(object):


    @staticmethod
    def get_currer_time(dateformat=None):
        """
        获取当前时间
        :param dateformat:
        :return:
        """
        # return time.strftime(dateformat, time.localtime(time.time()))
        return datetime.datetime.now()

    @staticmethod
    def get_file_time():
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())

    @staticmethod
    def get_unix_time(datetime):
        return int(time.mktime(datetime.timetuple()))
