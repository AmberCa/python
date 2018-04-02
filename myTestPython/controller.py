import utils
import getGRUResult
from flask import Flask

app = Flask(__name__)

@app.route('/<entity>')
def analysisEntities(entity):
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

if __name__  == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)


# #测试人人之间的关系
# data_info = {'string': '谈起曾经一起求学的日子,王大牛非常怀念他的师妹李晓华和韩梅梅', 'entities': [{'word': '王大牛', 'start': 12, 'end': 15, 'type': 'PER'}, {'word': '李晓华', 'start': 23, 'end': 26, 'type': 'PER'}, {'word': '韩梅梅', 'start': 27, 'end': 30, 'type': 'PER'}]}
# data_info = {'string': '堂姐杨诺思透露陈冠希与杨永晴感情未变，没有分手。', 'entities': [{'word': '杨诺思', 'start': 2, 'end': 5, 'type': 'PER'}, {'word': '陈冠希', 'start': 7, 'end': 10, 'type': 'PER'}, {'word': '杨永晴', 'start': 11, 'end': 14, 'type': 'PER'}]}
# analysisEntities(data_info)


#测试 人和手机之间的关系
# data_info = {'string': '李嘉欣的手机号码是15737135270', 'entities': [{'word': '李嘉欣', 'start': 0, 'end': 3, 'type': 'PER'}, {'word': '15737135270', 'start': 9, 'end': 20, 'type': 'PHONE'}]}
# analysisEntities(data_info)


# data_info = {'string': '陈慧琳和李嘉欣是好朋友，陈慧琳的联系方式18213645986。', 'entities':[{'word': '陈慧琳', 'start': 9, 'end': 12, 'type': 'PER'}, {'word': '18213645986', 'start': 34, 'end': 45, 'type': 'PHONE'}, {'word': '李嘉欣', 'start': 34, 'end': 45, 'type': 'PER'}]}
# analysisEntities(data_info)

# data_info = {'string': '90年代的娱乐大腕陈慧琳和李嘉欣非常被喜爱，陈慧琳的联系方式18213645986，李嘉欣的联系方式是15737135270。', 'entities': [{'word': '陈慧琳', 'start': 9, 'end': 12, 'type': 'PER'}, {'word': '15737135270', 'start': 51, 'end': 62, 'type': 'PHONE'}, {'word': '18213645986', 'start': 34, 'end': 45, 'type': 'PHONE'}, {'word': '李嘉欣', 'start': 13, 'end': 16, 'type': 'PER'}]}
# analysisEntities(data_info)
