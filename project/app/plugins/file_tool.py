#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/7 10:35
@Author     : libaojie
@File       : file_tool.py
@Software   : PyCharm
"""
import os


class FileTool(object):


    @staticmethod
    def mkdir_file(path):
        """
        创建文件的父菜单
        :param path:
        :return:
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))


    @staticmethod
    def write_file(path, content):
        """
        写信文件
        :param path:
        :param content:
        :return:
        """
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        # if os.path.isfile(path):
        #     os.remove(path)

        # 创建并打开一个新文件
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def clear_path(path):
        """
        清理文件
        :param path:
        :return:
        """
        if os.path.isdir(path):
            ls = os.listdir(path)
            for i in ls:
                c_path = os.path.join(path, i)
                FileTool.clear_path(c_path)
        elif os.path.isfile(path):
            os.remove(path)
