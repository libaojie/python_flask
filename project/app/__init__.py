#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 认证中心
@Time       : 2018/7/20 15:46
@Author     : libaojie
@File       : __init__.py
@Software   : PyCharm
"""
import os
import platform
import sys

from flask import Flask, Response, json
from flask_cors import CORS



app = Flask(__name__)
CORS(app, supports_credentials=True)


def __init_env():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    from project.config_tool import ConfigTool
    log_path = os.path.abspath(os.path.join(ConfigTool.get_path(), ConfigTool.get_str("logging", "path")))
    app.template_folder = os.path.abspath(os.path.join(ConfigTool.get_path(), "templates"))


def __init_config():
    # 加载配置
    from project.config_tool import ConfigTool
    app.config['DEBUG'] = ConfigTool.get_bool('flask', 'DEBUG')
    app.config['JSON_AS_ASCII'] = ConfigTool.get_str('flask', 'JSON_AS_ASCII')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ConfigTool.get_str('flask', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigTool.get_str('flask', 'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_BINDS'] = ConfigTool.get_dict('flask', 'SQLALCHEMY_BINDS')
    app.config['USE_RELOADER'] = ConfigTool.get_bool('flask', 'USE_RELOADER')
    app.config['SQLALCHEMY_ECHO'] = ConfigTool.get_bool('flask', 'SQLALCHEMY_ECHO')


def __init_log():
    # 初始化日志模块
    from project.config_tool import ConfigTool
    log_path = os.path.abspath(os.path.join(ConfigTool.get_path(), ConfigTool.get_str("logging", "path")))

    from project.app.plugins.log_tool import LogTool
    LogTool.init(log_path)
    LogTool.print("------------------启动项目-----------------------------")
    LogTool.print(f"平台信息：   【{platform.platform()}】")
    LogTool.print(f"当前路径：   【{os.getcwd()}】")
    LogTool.print(f"系统变量：   【{sys.path}】")
    LogTool.print(f"日志路径：   【{log_path}】")
    LogTool.print(f"main路径：   【{ConfigTool.get_path()}】")
    LogTool.print(f"python路径： 【{sys.executable}】")


def __init_db():
    from project.app.extensions import db
    db.init_app(app)
    db.app = app
    from project.app.common.database import DataBase
    from project.app.extensions import init_dataBase
    init_dataBase(DataBase(db))


def __init():
    __init_env()
    __init_config()
    __init_log()
    __init_db()


__init()


@app.route('/')
def index():
    """
    首页测试
    :return:
    """
    return 'security_center'
    # from project.app.plugins.utils import Utils
    # return Utils.get_post_json(0)


@app.route('/health')
def health():
    """
    心跳
    :return:
    """
    t = {'status': 'UP'}
    return Response(json.dumps(t), mimetype='application/json')


@app.before_request
def before_request():
    """
    全局请求过滤
    :return:
    """
    from project.app.plugins.util_tool import UtilTool
    return UtilTool.handle_request()


# @app.after_request
# def after_request(response):
#     """
#     全局返回过滤
#     :param response:
#     :return:
#     """
#     from project.app.plugins.utils import Utils
#     return Utils.handle_response(response)


# 注册蓝本
# 认证中心
from project.app.authority.api import blueprint_authority

app.register_blueprint(blueprint_authority)