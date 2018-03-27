#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest

from rmon.app import create_app
from rmon.models import Server
from rmon.models import db as database

@pytest.fixture
def app():
	"""
	Flask app
	"""
	return create_app()

@pytest.yield_fixture
def db(app):
	"""
	database
	"""
	with app.app_context():
		database.create_all()
		yield database
		database.drop_all()

@pytest.fixture
def server(db):
	"""
	测试 Redis 服务器记录
	"""
	server = Server(name='redis_test', description="this is a test record", host='123.5.6.4', port='6580')
	server.save()
	return server
