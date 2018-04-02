# import main


class NerControllerConfig(object):
	"""docstring for NerControllerConfig"""
	#实体提取
	# NER_CONTROLLER_FLAG = False
	# model = None
	# char_to_id = None
	# id_to_tag = None
	# sess = None
	# tf_config = None
	# entity_ckpy = None


	NER_CONTROLLER_FLAG = {'per':False, 'numType':False}
	model = {'per':None, 'numType':None}
	char_to_id = {'per':None, 'numType':None}
	id_to_tag = {'per':None, 'numType':None}
	sess = {'per':None, 'numType':None}
	tf_config = {'per':None, 'numType':None}
	entity_ckpy = {'per':None, 'numType':None}


# def test():
# 	# main.evaluate_line2()
# 	sentenceInfos = ['李晓华和她的丈夫王大牛，还有同事豆保军前日一起去英国旅行了', '王大牛命令李晓华在周末前完成这份代码。']
# 	for sentenceInfo in sentenceInfos:
# 		# print(sentenceInfo)
# 		print('---------------', sentenceInfo)
# 		entities = main.evaluate_line2(sentenceInfo)
# 		print('*'*10)
# 		print(entities)

# def test():
# 	print(NerControllerConfig.NER_CONTROLLER_FLAG['per'])NER_CONTROLLER_FLAG

# if __name__ == "__main__":
# 	test()