#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-20 16:50:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import numpy as np

class RelationConfig():
	
	__instance = None
	initData={}

	def __init__(self):
		print('@'*30)
		self.getWord2id()
		self.getRelation2Id()

	#singleton
	@classmethod
	def getInstance(cls):
		if not cls.__instance:
			cls.__instance = RelationConfig()
		return cls.__instance

	# def __new__(cls):
	# 	print(cls.__instance)
	# 	print(cls.__instance == None)
	# 	if not cls.__instance:
	# 		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
	# 		cls.__instance = object.__new__(cls)
	# 	return cls.__instance



	def getWord2id(self):
		print('reading word embedding data...')
		# vec = []
		word2id = {}
		with open('RE_BGRU_2ATT/origin_data/vec.txt', encoding='utf-8') as f:
		# f = open('RE_BGRU_2ATT/origin_data/vec.txt', encoding='utf-8')
			content = f.readline()
			content = content.strip().split()
			dim = int(content[1])
			while True:
				content = f.readline()
				if content == '':
					break
				content = content.strip().split()
				word2id[content[0]] = len(word2id)
				content = content[1:]
				content = [(float)(i) for i in content]
				# vec.append(content)
			f.close()
			word2id['UNK'] = len(word2id)
			word2id['BLANK'] = len(word2id)
			RelationConfig.initData['word2id'] = word2id

	def getRelation2Id(self):
		print('reading relation to id')
		#per2per
		self.getRelation2IdFactory('per_per')
		#per_phone
		self.getRelation2IdFactory('per_phone')
    
	def getRelation2IdFactory(self, type):
		relation2id = {}
		id2relation = {}
		with open('RE_BGRU_2ATT/origin_data/' + type + '/relation2id.txt', 'r', encoding='utf-8') as f:
			#f = open('./origin_data/per_per/relation2id.txt', 'r', encoding='utf-8')
			while True:
				content = f.readline()
				if content == '':
					break
				content = content.strip().split()
				relation2id[content[0]] = int(content[1])
				id2relation[int(content[1])] = content[0]
			f.close()
		wordembedding = np.load('RE_BGRU_2ATT/data/' + type + '/vec.npy')
		RelationConfig.initData[type + 'wordembedding'] = wordembedding
		RelationConfig.initData[type + 'relation2id'] = relation2id
		RelationConfig.initData[type + 'id2relation'] = id2relation

# t = RelationConfig()
# print(t)
# test = RelationConfig()
# print('test------------------%s'%test)
# test2 = RelationConfig.getInstance()

# print(test = test2)