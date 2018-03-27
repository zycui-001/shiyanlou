#!/usr/bin/env python3
# -*-coding:utf-8-*-

from collections import Mapping
from flask import request, Response, make_response
from flask.json import dumps
from flask.views import MethodView


class RestException(Exception):
	"""异常基类
	"""
	def __init__(self, code, message):
		"""初始化异常
		Aargs:
		    code (int): http 状态码
		    message (str): 错误信息
		"""
		self.code = code
		self.message = message
		super(RestException, self).__init__()

class RestView(MethodView):
	"""自定义 View 类
	json 序列化， 异常处理，装饰器支持
	"""
	content_type = 'application/json; charset=utf-8'
	method_decorators = []

	def handler_error(self, exception):
		"""处理异常
		"""
		data = {
		'ok': False,
		'message': exception.message
		}

		result = dumps(data) + '\n'
		resp = make_response(result, exception.code)
		resp.headers['Content-Type'] = self.content_type
		return resp

	def dispatch_request(self, *args, **kwargs):
		"""重写父类方法，支持数据自动序列化
		"""
		# 获取对应于 HTTP 请求方式的方法
		method = getattr(self, request.method.lower(), None)
		if method is None and request.method == 'HEAD':
			method = getattr(self, 'get', None)

		assert method is not None, 'Unimplemented method %r' % request.method

		# HTTP 请求方法定义了不同的装饰器
		if isinstance(self.method_decorators, Mapping):
			decorators = self.method_decorators.get(request.method.lower(), [])
		else:
			decorators = self.method_decorators
		for decorator in decorators:
			method = decorator(method)

		try:
			resp = method(*args, **kwargs)
		except RestException as e:
			resp = self.handler_error(e)

		# 如果返回结果已经是HTTP响应则直接返回
		if isinstance(resp, Response):
			return resp

		# 从返回值中解析出HTTP响应信息，比如状态码和头部
		data, code, headers = RestView.unpack(resp)

		# 处理错误，HTTP状态码大于400时认为是错误
		# 返回的错误类似于｛'name': ['redis server already exist']} 将其调整为
		# {'ok': False, 'message': 'redis server already exist'}
		if code >= 400 and isinstance(data. dict):
			for key in data:
				if isinstance(data[key], list) and len(data[key]) > 0:
					message = data[key][0]
				else:
					message = data[key]
			data = {'ok': False, 'message': message}

		# 序列话数据
		result = dumps(data) + '\n'
		# 生成 HTTP响应
		response = make_response(result, code)
		response.headers.extend(headers)

		# 设置响应头部为 application/json
		response.headers['Content-Type'] = self.content_type
		return response

	@staticmethod
	def unpack(value):
		"""解析试图方法返回值
		"""
		headers = {}
		if not isinstance(value, tuple):
			return value, 200, {}

		# 如果返回值有 3
		if len(value) == 3:
			data, code, headers = value
		elif len(value) == 2:
			data, code ==value
		return data, code, headers
