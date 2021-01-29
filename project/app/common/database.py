#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2018/10/10 10:49
@Author     : libaojie
@File       : database.py
@Software   : PyCharm
"""

from project.app.plugins.decorator import log_fun
from project.app.plugins.log_tool import LogTool


class DataBase(object):
    """
    数据库
    """

    def __init__(self, sqlAlchemy):
        """

        """
        if sqlAlchemy is None:
            LogTool.error('数据库无法连接！')
            return
        self.db_engine = sqlAlchemy.engine

    @log_fun
    def run_sql(self, sql):
        """
        执行sql列表
        :param sql_list:
        :return:
        """

        conn = self.db_engine.raw_connection()
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

    @log_fun
    def insert(self, sql, val):
        """
        执行插入
        :param sql:
        :param val:
        :return:
        """
        conn = self.db_engine.raw_connection()
        cursor = conn.cursor()  # 打开操作游标

        try:
            ret = cursor.executemany(sql, val)  # 执行数据插入操作
            conn.commit()  # 正常则提交
            return ret
        except Exception as e:
            conn.rollback()  # 异常则回滚
            LogTool.error("插入数据库报错：{0}".format(e))
            return None
        finally:
            cursor.close()
            conn.close()
            pass

    def get_insert_sql(self, tbl_name, columns):
        """conn
        组织多条记录入库的sql语句
        :param tbl_name: String 数据库表名
        :param columns: List 数据列名组成的列表
        :return:
        """
        _item = [':{0}']  # 定义展位符元素
        _items = _item * len(columns)  # 定义最终的占位符列表
        for i in range(len(_items)):
            _items[i] = _items[i].format(i + 1)

        _items_str = ','.join(_items)  # 获取列字符串
        _cols_str = ','.join(columns)  # 获取占位符字符串

        # 指定Insert语句的模板
        _insert_sql_fomat = """INSERT INTO {tbl_name}({cols}) VALUES({items})"""

        # 返回Insert语句
        return _insert_sql_fomat.format(tbl_name=tbl_name,
                                        cols=_cols_str,
                                        items=_items_str)

    def get_select_sql(self, tbl_name, columns=None):
        """
        获取查询语句
        :param tbl_name:
        :param columns:
        :return:
        """
        _col_str = '*'
        if columns is not None and len(columns) > 0:
            _col_str = ','.join(columns)

        _sql = 'select {0} from {1}'.format(_col_str, tbl_name)
        return _sql

    # @log_fun
    # def get_df_by_sql(self, sql):
    #     """
    #     通过sql语句获取dataframe
    #     :param sql:
    #     :return:
    #     """
    #     _ret = pd.read_sql(sql, con=self.db_engine)
    #     if _ret.empty:
    #         return None
    #     return _ret
