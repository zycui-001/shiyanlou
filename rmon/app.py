#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from flask import Flask 
from rmon.views import api
from rmon.models import db
from rmon.config import DevConfig, ProductConfig

def create_app():
	"""
	创建并初始化 Falsk app
	"""
	app = Flask('rmon')

	# 根据环境变量加载开发环境或生产环境配置
	env = os.environ.get('RMON_ENV')

	if env in ('pro', 'prod', 'product'):
		app.config.from_object(ProductConfig)
	else:
		app.config.from_object(DevConfig)

	# 从环境变量 RMON_SETTINGS 指定的文件中加载配置
	app.config.from_envvar('RMON_SETTINGS', silent=True)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# 注册Blueprint
	app.register_blueprint(api)
	# 初始化数据库
	db.init_app(app)
	# 如果是开发环境，则创建所有数据库表
	if app.debug:
		with app.app_content():
			db.create_all()
	return app
	


