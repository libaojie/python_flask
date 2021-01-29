
# Flask下mysqldb不支持python3，需要pymysql转一下
import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy.sql.default_comparator
import sqlalchemy.ext.baked

import gevent
from gevent import monkey
gevent.monkey.patch_all()