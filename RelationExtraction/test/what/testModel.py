#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-03-21 15:49:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os



class Test():

	myName = None
	__instance = None
	initData={}

	def __init__(self):
		print('@'*30)
		# Test.initData['a'] = 'a'
		# Test.initData['b'] = 'b'
		self.getdata()


	def __new__(cls):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def getdata(self):
		Test.initData['a'] = 'a'
		Test.initData['b'] = 'b'


# test = Test()
# print(test.initData)