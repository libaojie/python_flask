#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2018/7/2 14:56
@Author     : libaojie
@File       : extensions.py
@Software   : PyCharm
"""
from flask_sqlalchemy import SQLAlchemy

# 禁止自动提交
db = SQLAlchemy(session_options={"autoflush": False, "autocommit": False})



