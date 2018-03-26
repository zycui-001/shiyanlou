#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os

"""
rmon config
"""

class DevConfig:
	"""
	开发配置环境
	"""
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	TEMPLATES_AUTO_RELOAD = True

class ProductConfig(DevConfig):

	DEBUG = False

	#sqlite 数据库文件路径
	path = os.path.join(os.getcwd(), 'rmon.db').replace('\\', '/')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path 
