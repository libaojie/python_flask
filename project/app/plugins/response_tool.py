#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 响应工具
@Time       : 2019/2/28 9:21
@Author     : libaojie
@File       : response_tool.py
@Software   : PyCharm
"""
import os
from datetime import datetime

from flask import json, Response, make_response, send_from_directory
from sqlalchemy import text

from project.app.common import constant
from project.app.plugins.log_tool import LogTool
from project.app.plugins.type_tool import TypeTool


class ResponseTool(object):

    @staticmethod
    def handle_response(response):
        """
        最后处理response
        :return:
        """
        from project.app.plugins.db_tool import DBTool
        DBTool.session_commit()

        # if response.status_code == 200:
        #     if response.is_streamed:
        #         # 文件流处理
        #         DBTool.session_commit()
        #         return response
        #     val = json.loads(response.data)
        #     if val.__contains__('code') and val['code'] == 0 and not DBTool.session_commit():
        #         return ResponseTool.get_post_json(30)
        LogTool.info(f"##########请求结束##################")
        return response

    @staticmethod
    def get_post_json(code, msg=None, data=None):
        """
        返回json
        :param code:
        :param msg:
        :param data:
        :return:
        """
        LogTool.info(f'返回前端{code},{msg}')
        t = {}
        t['code'] = code
        if msg:
            t['msg'] = msg
        else:
            t['msg'] = constant.RESPONSE_CODE_INFO[code]

        if data:
            if isinstance(data, dict):
                # 字典类型
                if data.__contains__('total'):
                    t['total'] = data['total']
                if data.__contains__('per_page'):
                    t['per_page'] = data['per_page']
                if data.__contains__('items'):
                    t['data'] = ResponseTool.get_dict_value(data['items'])
                else:
                    t['data'] = ResponseTool.get_dict_value(data)
            else:
                # 其他类型
                t['data'] = ResponseTool.get_dict_value(data)

        _ret = json.dumps(t)
        return Response(_ret, mimetype='application/json')

    @staticmethod
    def get_dict_value(param):
        """
        获取字典值
        :param param:
        :return:
        """
        from project.app.model.model import EntityBase

        def _f(param):
            if param is None:
                return ''
            elif isinstance(param, str):
                return param
            elif isinstance(param, int):
                return param
            elif isinstance(param, datetime):
                return param.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(param, dict):
                ret = {}
                for key, val in param.items():
                    ret[key] = _f(val)
                return ret
            elif isinstance(param, list):
                return [_f(val) for val in param]
            elif isinstance(param, EntityBase):
                return param.as_dict()

        return _f(param)

    @staticmethod
    def download_file(fpath):
        """
        下载文件
        :param fpath:
        :return:
        """
        if not os.path.exists(fpath):
            return ResponseTool.get_post_json(140402)  # 文件目录不存在

        if os.path.isfile(fpath):
            filepath, fullflname = os.path.split(fpath)  # 分割目录和文件名
            response = make_response(send_from_directory(filepath, fullflname, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                fullflname.encode().decode('latin-1'))
            return response
        else:
            return ResponseTool.get_post_json(140401)  # 不是文件

    @staticmethod
    def return_page(data, total, page, per_page):
        """
        分页返回结果
        :param data:
        :param total:
        :param pre_page:
        :return:
        """

        _return_data = {'items': data}
        if page:
            _return_data['total'] = total
            _return_data['per_page'] = per_page
        return _return_data

    @staticmethod
    def return_page_by_query(model, page, per_page, precise_list=None, fuzzy_list=None):
        """
        获取返回分页信息
        :param query:
        :param page:
        :param per_page:
        :return:
        """
        query = model.query
        # 排序
        query.order_by(model.create_time.desc())

        # 精准查询字段
        if precise_list and isinstance(precise_list, list) and len(precise_list) > 0:
            for precise in precise_list:
                if isinstance(precise, dict):
                    for key, value in precise.items():
                        if not hasattr(model, key):
                            LogTool.error(f"{model.__tablename__}表找不到{key}字段")
                            continue
                        if value:
                            query = query.filter(text(f"{key} = '{value}'"))

        # 模糊查询
        if fuzzy_list and isinstance(fuzzy_list, list) and len(fuzzy_list) > 0:
            for fuzzy in fuzzy_list:
                if isinstance(fuzzy, dict):
                    for key, value in fuzzy.items():
                        if not hasattr(model, key):
                            LogTool.error(f"{model.__tablename__}表找不到{key}字段")
                            continue
                        if value:
                            query = query.filter(text(f"{key} like '%{value}%'"))

        if page:
            page = TypeTool.change_to_int(page)
            if page is None:
                page = 1

            if per_page is None:
                from project.app.model.data_dict import DataDict
                dataDict = DataDict.get_value_by_code_key(constant.PAGE_CODE, constant.PAGE_KEY)
                if dataDict is None:
                    LogTool.error(f"找不到分页数据字典项：{constant.PAGE_CODE} {constant.PAGE_KEY}")
                else:
                    per_page = dataDict.dict_val

            per_page = TypeTool.change_to_int(per_page)
            if per_page is None:
                per_page = 10

            query = query.paginate(page, per_page, error_out=False)
            return ResponseTool.return_page(query.items, query.total, page, per_page)
        else:
            return ResponseTool.return_page(query.all(), None, None, None)


