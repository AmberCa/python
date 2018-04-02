class User():
	
	__instance = None

	def __init__(self, name):
		self.name = name

	def __new__(cls, name):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

u1 = User('zhangsan') 
u2 = User('lisi')

print(u1.name, u2.name)
print(u1 == u2, u1, u2)

print('-'*30)


class Stu():
	
	__instance = None

	def __init__(self, name):
		self.name = name
	
	@classmethod
	def getInstance(cls, name):
		if not cls.__instance:
			cls.__instance = Stu(name)
		return cls.__instance


s1 = Stu.getInstance('s1')
s2 = Stu.getInstance('s2')

print(s1.name, s2.name)
print(s1 == s2, s1, s2)


