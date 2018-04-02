'''
name = "abc efg\thijk\tlmn\nxwzy\nuvw"
print("分割前：%s"%name)
name = name.split()
print("分割后：",end=" ")
print(name)
'''
vec = ['a','b']
content = [1,2,4,5,3]
print(content)
content = [float(i) for i in content]
print(content)
vec.append(content)
print(vec)
