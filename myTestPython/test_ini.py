import configparser

config = configparser.ConfigParser()
config.read("propertis.ini")

name = config.get('detail', 'name')
age = config.get('detail', 'age')
sex = config.get('detail','sex')

address = config.get('add', 'address')

print(name + '\t' + age + '\t' + sex + '\t' + address)
