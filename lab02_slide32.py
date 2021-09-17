#!/usr/bin/python3
num = int(input('Enter a number:\n'))
num_decimal = num
bit_string = ''
while num > 0:
	if num & 1 > 0:
		bit_string = '1' + bit_string
	else:
		bit_string = '0' + bit_string
	num = num >> 1
print(bit_string)

count = 0
for x in range(0, len(bit_string)):
    if (num_decimal & 2**x > 0):
        count += 1

print(count)

