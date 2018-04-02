from flask import Flask, request, url_for, render_template

app = Flask(__name__)

class myClass():
	testStr = '1'

@app.route('/myTest/<number>')
def myTest(number):
	print('this is myClass.testStr----%s'%myClass.testStr)
	if myClass.testStr == '1':
		print(number)
		print('this is 1')
		myClass.testStr = '2'
	else:
		print('this not 1 number ---%s'%number)
		print('this is not 1')
	return number

@app.route('/<name>')
def hellWorld(name=None):
	print(name)
	#return render_template('hello.html', name=name)
	#return '<h1>Hello World</h1>'

@app.route('/user/<username>')
def getUsername(username):
	print('-'*6, request.args.get('username'))
	print(request.method)
	print('-----------', url_for('testUrlFor'))
	return 'User %s'%username

@app.route('/test')
def testUrlFor():
	print('-'*6, 'url_for')

if __name__  == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)
	#app.debug = True
	#app.run()
