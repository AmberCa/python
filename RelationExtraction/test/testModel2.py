#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-03-21 17:05:33
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from what import testModel
from what import testModel3
from flask import Flask
import myTest
from config import config


app = Flask(__name__)

# app.config.from_object(config['development'])  
test = testModel.Test()
# config['development'].init_app(app) 
print(app.config)
# print(app.config['development'])


@app.route('/test')
def test():
	testModel3.test()
	return "success"

if __name__  == '__main__':
	
	testModel3.modelOneName()
	print(test)
	app.run(host='0.0.0.0', port=9000, debug=True)
