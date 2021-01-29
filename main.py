#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/5/22 10:01
@Author     : libaojie
@File       : main.py
@Software   : PyCharm
"""
import os
import sys

from gunicorn.app.base import Application

from project.config_tool import ConfigTool

try:
    mainroot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    mainroot = os.path.dirname(os.path.abspath(sys.argv[0]))

ConfigTool.set_path(mainroot)

from project.app import app

options = {
    'bind': ConfigTool.get_str('gunicorn', 'bind'),
    'workers': ConfigTool.get_int('gunicorn', 'workers'),
    'threads': ConfigTool.get_int('gunicorn', 'threads'),
    'daemon': ConfigTool.get_str('gunicorn', 'daemon'),
    'worker_class': ConfigTool.get_str('gunicorn', 'worker_class'),
    'worker_connections': ConfigTool.get_int('gunicorn', 'worker_connections'),
    'accesslog': ConfigTool.get_str('gunicorn', 'accesslog'),
    'errorlog': ConfigTool.get_str('gunicorn', 'errorlog'),
    'loglevel': ConfigTool.get_str('gunicorn', 'loglevel'),
}


class GunicornRunner(Application):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornRunner, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


GunicornRunner(app, options).run()
