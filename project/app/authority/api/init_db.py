#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/9 10:21
@Author     : libaojie
@File       : init_db.py
@Software   : PyCharm
"""
import os

from flask import render_template, request, redirect, make_response, send_file

from project.app import blueprint_authority
from project.app.plugins.db_tool import DBTool
from project.app.plugins.decorator import except_fun
from project.app.plugins.file_tool import FileTool
from project.app.plugins.util_tool import UtilTool
from project.config_tool import ConfigTool


@except_fun
@blueprint_authority.route("/initDB", methods=["GET"])
def initBD_get():
    return render_template("init_db.html")


@blueprint_authority.route("/initDB", methods=["POST"])
def initDB_post():
    f = request.files['file']
    uuid = UtilTool.get_file_time()
    # upload_path = os.path.join(ConfigTool.get_path(), r"data\uploads", uuid, secure_filename(f.filename))
    upload_path = os.path.join(ConfigTool.get_path(), r"data\uploads", uuid)

    excel_path = os.path.join(upload_path, f.filename)
    out_path = os.path.join(upload_path, "init_db.sql")
    FileTool.mkdir_file(excel_path)

    # 保存Excel
    f.save(excel_path)

    # # 处理Excel
    # handleExcel = HandleExcel(excel_path, out_path)
    # handleExcel.run()

    # 是否初始化数据库
    if request.form.__contains__('db') and request.form['db'] == 'on':
        clear_sql = ["delete from CA_USER",
                     "delete from CA_USER_ROLE",
                     "delete from CA_SYS_LOG",
                     "delete from CA_APPLICATION",
                     "delete from CA_ORG",
                     "delete from CA_DICT",
                     "delete from CA_GROUP",
                     "delete from CA_GRP_ROLE",
                     "delete from CA_MENU",
                     "delete from CA_ROLE_MENU",
                     "delete from CA_ROLE",
                     "delete from CA_SERVICE",
                     "delete from CA_ROLE_SERV",
                     "delete from CA_USER_GRP",
                     "delete from CA_MENU_SERV",
                     ]

        for sql in clear_sql:
            ret = DBTool.run_sql(sql)
            pass


    if os.path.isfile(out_path):
        # 存在文件
        response = make_response(send_file(out_path))
        return response

    return redirect("result")


@blueprint_authority.route("/result", methods=["GET"])
def result():
    return render_template("result.html", result="success")