import os
import shutil
import itertools
import getGRUResult

def make_path(params):
	if not os.path.isdir('data/'+params):
		os.makedirs('data/'+params)
	if not os.path.isdir('model/'+params):
		os.makedirs('model/'+params)
	if not os.path.isdir('origin_data/'+params):
		os.makedirs('origin_data/'+params)

def clean(params):
	"""
	Clean current folder
	remove saved model and training log
	"""
	if os.path.isdir('model/'+params):
		shutil.rmtree('model/'+params)
	if not os.path.isdir('model/'+params):
		os.makedirs('model/'+params)

def getClassNum(modelPath):
	modelPaht_classNum = {'per_phone' : 13, 'per_per' : 12}
	return modelPaht_classNum.get(modelPath)

def getModelPath(entityType):
	modelPath = {'per_per' : './model/per_per/ATT_GRU_model', 
				'per_phone' : './model/per_phone/ATT_GRU_model'}
	return modelPath.get(entityType)

#单个模型组合
def singleModel(modelList):
	#list1 = ['张三','李四','王五']
	list2 = []
	iter = itertools.combinations(modelList,2)
	for i in iter:
		list2.append(i)
	return list2


#多个模型进行组合
def moreModel(modelList1, modelList2):
	# I=[1,2,3]#,4,5,6,7,8,9,10
	# J=['spades','hearts']#,'diamonds','clubs'
	# dataResult = [(i,j)for i in modelList1 for j in modelList2]
	# for i in dataResult:
	# 	print(i)
	return [(i,j) for i in modelList1 for j in modelList2]

# list1 = ['dbj', 'ca', 'djw']
# list2 = [1, 2 , 3]
# dataResult = moreModel(list1, list2)
# print(dataResult)
