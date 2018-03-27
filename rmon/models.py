#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from redis import StrictRedis, RedisError
from rmon.common.rest import RestException


db = SQLAlchemy()

class Server(db.Model):
	__tablename__ = 'redis_server'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	description = db.Column(db.String(512))
	host = db.Column(db.String(15))
	port = db.Column(db.Integer, default=6379)
	password = db.Column(db.String())
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 该方法使得我们在通过print(server_instance)这样的语句打印server实例显示服务器名称信息
	def __repr__(self):
		return '<Server(name=%s)>' % self.name

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	@property 
	def redis(self):
		return StrictRedis(host=self.host, port=self.port, password=self.password, socket_timeout=5)

	def ping(self):
		"""检查 Redis 服务器监控信息
		"""
		try:
			return self.redis.ping()
		except RedisError:
			raise RestException(400, 'redis server %s can not connected' % self.host)

	def get_metrics(self):
		"""获取 Redis 服务器监控信息
        通过 Redis 服务器指令 INFO 返回监控信息
		"""
		try:
			return self.redis.info()
		except RedisError:
			raise RestException(400, 'redis server %s can not connected' % self.host)
	

		
