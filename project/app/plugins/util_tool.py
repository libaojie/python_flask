#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 工具箱
@Time       : 2018/7/20 16:20
@Author     : libaojie
@File       : utils.py
@Software   : PyCharm
"""
import uuid


class UtilTool(object):
    """
    工具类
    """

    @staticmethod
    def get_uuid():
        """
        获取uuid
        :return:

        """
        return uuid.uuid1().hex.upper()

    @staticmethod
    def is_null(val):
        '''
        检测不明类型是否为空
        :param val:
        :return:
        '''
        if val is None:
            return True

        if isinstance(val, str) and val.strip() == '':
            return True

        if isinstance(val, list) and len(val) == 0:
            return True

        return False
