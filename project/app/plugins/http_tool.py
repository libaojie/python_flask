#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/9 10:26
@Author     : libaojie
@File       : http_tool.py
@Software   : PyCharm
"""
import json

import requests

from project.app.plugins.log_tool import LogTool


class HttpTool(object):

    @staticmethod
    def request_get(url, payload):
        val = None
        LogTool.info(f"网络get发包：url:【{url}】, payload：【{payload}】")
        respone = requests.get(url, params=payload)
        LogTool.info(f"网络get收包：respone:【{str(respone)}】")
        if respone.status_code == 200:
            val = json.loads(respone.text)
            LogTool.info(f"网络包解析:【{val}】")
        return val

    @staticmethod
    def request_post(url, payload):
        val = None
        header = {
            "Content-Type": "application/json"
        }
        LogTool.info(f"网络post发包：url:【{url}】, payload：【{payload}】")
        respone = requests.post(url, headers=header, json=payload)
        LogTool.info(f"网络get收包：respone:【{str(respone)}】")
        if respone.status_code == 200:
            val = json.loads(respone.text)
            LogTool.info(f"网络包解析:【{val}】")
        return val
