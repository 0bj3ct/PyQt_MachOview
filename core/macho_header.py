# -*- coding: utf-8 -*-
#file: macho_header.py
#author: 0bj3ct
#description: macho文件格式头解析模块

import sys

class macho_header_t(object):
	"""docstring for macho_header_t"""
	def __init__(self, arg):
		super(macho_header_t, self).__init__()
		self.arg = arg
		