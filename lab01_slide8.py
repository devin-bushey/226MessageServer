#!/usr/bin/python3

temp = int(input('Enter a water temperature:\n'))
if temp < 0:
	print('Below freezing point')
elif temp == 0:
	print('Frezing')
else:
	print('Above freezing point')

