#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-03-21 17:09:35
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import sys
import os
sys.path.append(os.getcwd()+'/what')
print(os.getcwd())
print(sys.path)
import testModel
import testModel2
import myTest




def test():
	print('-----------%s'%testModel.Test.myName)
	myTest.myTestFunction()
	print('------------%s'%testModel2.test.initData)

def modelOneName():
	print('modelOneName----------------')
	testModel.Test.myName = 'dbj'