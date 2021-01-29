#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2018/12/3 14:25
@Author     : libaojie
@File       : db_tool.py
@Software   : PyCharm
"""
from sqlalchemy.exc import SQLAlchemyError

from project.app.extensions import db
from project.app.plugins.log_tool import LogTool


class DBTool(object):
    __instance = None  # 定义一个类属性做判断

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance == object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    @classmethod
    def __get_conn(cls):

        if db is not None and db.engine is not None:
            return db.engine.raw_connection()

    @classmethod
    def run_sql(cls, sql):
        """
        执行sql列表
        :param sql_list:
        :return:
        """

        conn = cls.__get_conn()
        cursor = conn.cursor()  # 打开操作游标

        try:
            LogTool.info('执行sql：{0}'.format(sql))
            ret = cursor.execute(sql)  # 执行数据插入操作
            if ret:
                ret = (ret.description, list(ret.fetchall()))
            conn.commit()  # 正常则提交
            return True, ret
        except Exception as e:
            conn.rollback()  # 异常则回滚
            LogTool.error("执行数据库报错，报错信息：{0}\n\t\t\t\t\t\t\t报错语句：{2}".format(e, sql))
            return False, None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def session_commit(cls):
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            reason = str(e)
            LogTool.error(reason)
            return False
