#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 请求工具
@Time       : 2019/2/28 9:18
@Author     : libaojie
@File       : request_tool.py
@Software   : PyCharm
"""
from flask import request

from project.app.common import constant
from project.app.plugins.db_tool import DBTool
from project.app.plugins.log_tool import LogTool
from project.app.plugins.response_tool import ResponseTool
from project.app.plugins.type_tool import TypeTool


class RequestTool(object):

    @staticmethod
    def handle_request():
        """
        预处理request
        :return:
        """
        LogTool.info("----------请求开始----------")
        # if request is None:
        #     LogTool.error('前端未发送request！')
        #     return ResponseTool.get_post_json(21)
        #
        # LogTool.info(f'url:【{request.path}】 model:【{request.method}】')
        #
        # if request.path not in constant.IGNORE_URL:
        #     # POST、PUT方式必须以json方式提交
        #     if request.method in ['POST', 'PUT']:
        #         if not 'application/json' in request.content_type:
        #             LogTool.error(f"数据传输格式有误！ method:【{request.method}】 content_type:【{request.content_type}】")
        #             return ResponseTool.get_post_json(22)
        #         else:
        #             try:
        #                 json = request.json
        #             except Exception as err:
        #                 LogTool.error(f"传输的json格式有误【{request.data}】")
        #                 return ResponseTool.get_post_json(23)
        #
        #         LogTool.info(f'value:【{request.json}】')
        #     else:
        #         LogTool.info(f'value:【{request.args}】')
        return None


    @staticmethod
    def get_request_page(request):
        """
        获取分页信息
        :param request:
        :return:
        """
        page = request.args.get('page')
        per_page = request.args.get('per_page')

        page = TypeTool.change_to_int(page)
        per_page = TypeTool.change_to_int(per_page)

        if page != None and page == 0:
            page = None
            per_page = None
        if page == None:
            per_page = None
        if page and not per_page:
            per_page = int(DBTool.get_page_row(constant.DEFAULT_PRE_PAGR))
        return page, per_page
