import os
import sys
sys.path.append(os.getcwd()+ '/RE_BGRU_2ATT')
print(sys.path)
import utils
import getGRUResult


def relationExtract(entity):

	print('entity-------------', entity)
	# analysis all entities
	per_list = []
	phone_list = []

	sentence = entity.get('string')
	entities = entity.get('entities')
	for entity in entities:
		type_entity = entity.get('type')
		if 'PER' == type_entity:
			per_list.append(entity.get('word'))
		elif 'PHONE' == type_entity:
			phone_list.append(entity.get('word'))
		else:
			pass

	if len(per_list) > 1:
		per_list2 = utils.singleModel(per_list)
		print('--------%s'%per_list2)
		getGRUResult.getRelation('per_per', per_list2, sentence)
	if len(phone_list) >= 1 and len(per_list) >= 1:
		data_list = utils.moreModel(per_list, phone_list)
		print('--------%s'%data_list)
		getGRUResult.getRelation('per_phone', data_list, sentence)



# #测试人人之间的关系
# data_info = {'string': '这篇论文是王大牛负责编程，李晓华负责写作的', 'entities': [{'word': '王大牛', 'start': 12, 'end': 15, 'type': 'PER'}, {'word': '李晓华', 'start': 23, 'end': 26, 'type': 'PER'}]}
data_info = {'string': '这篇论文是王大牛负责编程，李晓华和韩梅梅负责写作的。', 'entities': [{'word': '王大牛', 'start': 12, 'end': 15, 'type': 'PER'}, {'word': '李晓华', 'start': 23, 'end': 26, 'type': 'PER'}, {'word': '韩梅梅', 'start': 27, 'end': 30, 'type': 'PER'}]}

# data_info = {'string': '消息透露陈冠希与杨永晴感情未变，没有分手。', 'entities': [{'word': '陈冠希', 'start': 7, 'end': 10, 'type': 'PER'}, {'word': '杨永晴', 'start': 11, 'end': 14, 'type': 'PER'}]}
# data_info = {'string': '堂姐杨诺思透露陈冠希与杨永晴感情未变，没有分手。', 'entities': [{'word': '杨诺思', 'start': 2, 'end': 5, 'type': 'PER'}, {'word': '陈冠希', 'start': 7, 'end': 10, 'type': 'PER'}, {'word': '杨永晴', 'start': 11, 'end': 14, 'type': 'PER'}]}
# data_info = {'string': '联想集团的总部位于北京,首席执行官是杨元庆先生，其联系方式是15865462212', 'entities': [{'word': '杨元庆', 'start': 7, 'end': 10, 'type': 'PER'}, {'word': '15865462212', 'start': 11, 'end': 14, 'type': 'PHONE'}]}



#测试 人和手机之间的关系
# data_info = {'string': '李嘉欣的手机号码是15737135270', 'entities': [{'word': '李嘉欣', 'start': 0, 'end': 3, 'type': 'PER'}, {'word': '15737135270', 'start': 9, 'end': 20, 'type': 'PHONE'}]}

# data_info = {'string': '在昨天的直播中，冯提莫公开了自己的手机号15685214863', 'entities': [{'word': '冯提莫', 'start': 0, 'end': 3, 'type': 'PER'}, {'word': '15685214863', 'start': 9, 'end': 20, 'type': 'PHONE'}]}


# data_info = {'string': '陈慧琳和李嘉欣两个人前日一起去英国旅行。，陈慧琳的联系方式18213645986。', 'entities':[{'word': '陈慧琳', 'start': 9, 'end': 12, 'type': 'PER'}, {'word': '18213645986', 'start': 34, 'end': 45, 'type': 'PHONE'}, {'word': '李嘉欣', 'start': 34, 'end': 45, 'type': 'PER'}]}

# data_info = {'string': '90年代的娱乐大腕陈慧琳和李嘉欣非常被喜爱，陈慧琳的联系方式18213645986，李嘉欣的联系方式是15737135270。', 'entities': [{'word': '陈慧琳', 'start': 9, 'end': 12, 'type': 'PER'}, {'word': '15737135270', 'start': 51, 'end': 62, 'type': 'PHONE'}, {'word': '18213645986', 'start': 34, 'end': 45, 'type': 'PHONE'}, {'word': '李嘉欣', 'start': 13, 'end': 16, 'type': 'PER'}]}

relationExtract(data_info)
