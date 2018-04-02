def digui(number):
	if number == 1:
		return 1
	else:
		return number*digui(number-1)
number = int(input("请输入阶乘："))
print(number)
print(isinstance(number,(int)))
sum2 = digui(number)
print("sum2---%s"%sum2)
