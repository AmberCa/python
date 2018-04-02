
#coding=utf-8
import json
from NER_IDCNN_CRF import main
from RE_BGRU_2ATT import GRUcontroller
from RE_BGRU_2ATT import relationConfig
from flask import Flask, request, url_for, render_template

app = Flask(__name__)

# relation = None

def testSentence(sentenceInfo):
	modelTpye=['per', 'numType']
	result = []
	entities = {'string':sentenceInfo, 'entities':[]}
	print('---------------', sentenceInfo)
	for model in modelTpye:
		entities1 = main.getEntity6(sentenceInfo, model)
		if len(entities['entities']) == 0:
			entities['entities'] = entities1['entities']
		else:
			for entity in entities1['entities']:
				entities['entities'].append(entity)

	print('*'*10)
	print(entities)
	result.append(entities)
	resultList = GRUcontroller.relationExtract(entities)
	result.append(resultList)

	print(result)
	return result

def test2():
	sentenceInfos = ['李晓华和她的丈夫王大牛，还有同事张小明前日一起去英国旅行了'
		, '王大牛命令李晓华在周末前完成这份代码。','王小明非常疼爱他的孙女韩梅梅小朋友。']
	for sentenceInfo in sentenceInfos:
		print(sentenceInfo)
		result = testSentence(sentenceInfo)


# if __name__ == "__main__":
# 	# relation = relationConfig.RelationConfig.getInstance()
# 	# print(relation.initData)
# 	test2()

@app.route('/testJs',methods=['POST','GET'])#/<sentenceInfo>
def testJs():
	print('request.form--------------------%s'%request.form['sentence'])
	sentenceInfo = request.form['sentence']
	result = testSentence(sentenceInfo)
	result = json.dumps(result, ensure_ascii=False)
	print('json.dumps(result, ensure_ascii=False)----------%s'%result)
	return json.dumps(result, ensure_ascii=False)



@app.route('/test/<number>')
def test(number):
	print("-------------------------%s"%number)
	if number == '1':
		sentenceInfo = '王大牛命令李晓华在周末前完成这份代码。'
	else:
		sentenceInfo = '王小明非常疼爱他的孙女韩梅梅小朋友。'
	result = testSentence(sentenceInfo)
	return render_template('helloFlask.html', title = '实体识别和关系提取的结果', 
		entity = result[0]['entities'], relation = result[1])


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/hello/<name>')
def getName(name):
	#json 解码
	name = json.loads(name)
	print('name----%s'%name)
	test = {"1":123, "2":"testName", "name":"李嘉欣"}
	# test = json.loads(test)
	#json 转码
	return json.dumps(test, ensure_ascii=False)#解决中文乱码 ensure_ascii=False


if __name__  == '__main__':
	# main.getEntity("王大牛命令李晓华在周末前完成这份代码。")
	# relation = relationConfig.RelationConfig()
	# relation = relationConfig.RelationConfig.getInstance()
	# print('RelationConfig------------%s'%relation)
	app.run(host='0.0.0.0', port=9000, debug=True)