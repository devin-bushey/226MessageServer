#!/usr/bin/python3

n = int(input('Enter a number:\n'))
i = 2
result = ""

while i * i <= n:
    if n % i == 0:
        result = str(n) + ' is not a prime'
        break
        
    else:
        result = str(n) + ' is a prime'
        
    i = i + 1

print(result)


