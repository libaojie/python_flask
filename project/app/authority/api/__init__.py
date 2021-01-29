#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 蓝图
@Time       : 2018/7/20 15:50
@Author     : libaojie
@File       : __init__.py
@Software   : PyCharm
"""

from flask import Blueprint

blueprint_authority = Blueprint("api_authority", __name__, url_prefix='/ca')


@blueprint_authority.before_request
def before_request():
    """
    当前蓝图拦截
    :return:
    """
    return None

from . import init_db


