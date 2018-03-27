#!/usr/bin/env python3
# -*-coding:utf-8-*-

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
