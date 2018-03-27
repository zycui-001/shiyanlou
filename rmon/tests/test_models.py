#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from rmon.models import Server
from rmon.common.rest import RestException

class TestServer:
	"""测试 Server 相关功能 
	"""
	def test_save(self, db):
		"""测试 Server.save 保存服务器方法
		"""
		# 初始状态下，数据库中没有保存任何 Redis， 所以数量为0
		assert Server.query.count() == 0
		server = Server(name='test', host='127.0.0.1')
		# 保存到数据库中
		server.save()
        # 现在数据库中的数量变为1
		assert Server.query.count() == 1
		# 且数据库中的记录就算之前创建的记录
		assert Server.query.first() == server

	def test_delete(self, db, server):
		"""测试 Server.delete 删除服务器方法
		"""
		assert Server.query.count() == 1
		server.delete()
		assert Server.query.count() == 0

	def test_ping_success(self, db, server):
		"""test
		"""
		assert server.ping() is True

	def test_ping_failed(self, db):
		"""test
		"""
		server = Server(name='test', host='127.0.0.1', port=6399)

		try:
			server.ping()
		except RestException as e:
			assert e.code == 400
			assert e.message == 'redis server %s can not connected' % server.host
			
