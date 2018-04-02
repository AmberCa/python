class Test:

	def	__init__(self):
		self.name = 'dbj'
		self.age = '28'
		self.__pwd = '123456'

	def get__pwd(self):
		return self.__pwd

	def __str__(self):
		print(self.name, self.age, self.__pwd)
		return self.name + ' ' + self.age + ' ' + self.__pwd

class Animal:

	name = 'animal'
	__pwd = '123'

	def get__pwd(self):
		return self.__pwd

class Dog(Animal):

	pass

print(Dog.name)
a = Animal()
print(Animal.name, a.get__pwd())

#test = Test()
#print(test.name, ' ', test.age, ' ', test.get__pwd())
#print(test)
