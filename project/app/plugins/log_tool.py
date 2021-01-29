#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    :
@Time       : 2018/8/15 15:36
@Author     : libaojie
@File       : log_tool.py
@Software   : PyCharm
"""
import logging
import os
import shutil
import time
import zipfile


class LogTool(object):
    __instance = None  # 定义一个类属性做判断
    path = None
    handler = None
    errhandler = None
    logger = None
    day = None
    max_length = 300
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL, }

    def __new__(cls):
        if cls.__instance is None:
            # 如果__instance为空证明是第一次创建实例
            # 通过父类的__new__(cls)创建实例
            cls.__instance == object.__new__(cls)
            return cls.__instance
        else:
            # 返回上一个对象的引用
            return cls.__instance

    @classmethod
    def init(cls, path):
        """
        初始化
        :param path:
        :return:
        """
        cls.path = path
        cls.logger = logging.getLogger()
        level = 'default'
        cls.logger.setLevel(cls.levels.get(level, logging.NOTSET))

    @classmethod
    def check_day(cls):
        cur_day = cls.getCurrentDay()

        if cls.day:
            if cur_day != cls.day:
                # 压缩过去一天
                cls.zip_file_path(os.path.join(cls.path, cls.day))
                # 新一天
                cls.get_handler(cur_day)
                # 删除过去一天
                cls.delete_file_path(os.path.join(cls.path, cls.day))
        else:
            cls.get_handler(cur_day)
        cls.day = cur_day

    @classmethod
    def get_handler(cls, day):
        log_filename = os.path.join(cls.path, day, 'log.log')
        err_filename = os.path.join(cls.path, day, 'error.log')
        cls.createFile(log_filename)
        cls.createFile(err_filename)
        # 注意文件内容写入时编码格式指定
        cls.handler = logging.FileHandler(log_filename, encoding='utf-8')
        cls.errhandler = logging.FileHandler(err_filename, encoding='utf-8')

    @classmethod
    def createFile(cls, filename):
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        if not os.path.isfile(filename):
            # 创建并打开一个新文件
            fd = open(filename, mode='w', encoding='utf-8')
            fd.close()

    # logger可以看做是一个记录日志的人，对于记录的每个日志，他需要有一套规则，比如记录的格式（formatter），
    # 等级（level）等等，这个规则就是handler。使用logger.addHandler(handler)添加多个规则，
    # 就可以让一个logger记录多个日志。

    @classmethod
    def setHandler(cls, level):
        cls.check_day()
        if level == 'error':
            cls.logger.addHandler(cls.errhandler)
        # 把logger添加上handler
        cls.logger.addHandler(cls.handler)

    @classmethod
    def removerhandler(cls, level):
        if level == 'error':
            cls.logger.removeHandler(cls.errhandler)
        cls.logger.removeHandler(cls.handler)

    @classmethod
    def getCurrentTime(cls):
        dateformat = '%Y-%m-%d %H:%M:%S'
        return time.strftime(dateformat, time.localtime(time.time()))

    @classmethod
    def getCurrentDay(cls):
        dateformat = '%Y-%m-%d'
        return time.strftime(dateformat, time.localtime(time.time()))

    # 静态方法
    @staticmethod
    def print(log_message):
        print(log_message)
        LogTool.info(log_message)

    # 静态方法
    @staticmethod
    def debug(log_message):
        LogTool.setHandler('debug')
        LogTool.logger.debug("[DEBUG " + LogTool.getCurrentTime() + "]" + log_message)
        LogTool.removerhandler('debug')

    @staticmethod
    def info(log_message):
        LogTool.setHandler('info')
        LogTool.logger.info("[INFO " + LogTool.getCurrentTime() + "]" + log_message)
        LogTool.removerhandler('info')

    @staticmethod
    def warning(log_message):
        LogTool.setHandler('warning')
        LogTool.logger.warning("[WARNING " + LogTool.getCurrentTime() + "]" + log_message)
        LogTool.removerhandler('warning')

    @staticmethod
    def error(log_message):
        LogTool.setHandler('error')
        _log = "[ERROR " + LogTool.getCurrentTime() + "]" + log_message
        print(_log)
        LogTool.logger.error(_log)
        LogTool.removerhandler('error')

    @staticmethod
    def critical(log_message):
        LogTool.setHandler('critical')
        LogTool.logger.critical("[CRITICAL " + LogTool.getCurrentTime() + "]" + log_message)
        LogTool.removerhandler('critical')

    @classmethod
    def zip_file_path(cls, input_path):
        """
        压缩文件夹
        :param input_path:
        :return:
        """
        output_name = input_path + '.zip'
        z = zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(input_path):
            fpath = dirpath.replace(input_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()

    @classmethod
    def delete_file_path(cls, input_path):
        """
        删除原文件夹
        :param input_path:
        :return:
        """
        # for dirpath, dirnames, filenames in os.walk(input_path):
        #     for filename in filenames:
        #         if os.path.isfile(filename):
        #             try:
        #                 os.remove(filename)
        #             except os.error:
        #                 pass
        if os.path.isdir(input_path):
            shutil.rmtree(input_path)

