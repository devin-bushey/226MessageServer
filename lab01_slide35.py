#!/usr/bin/python3

i = 2

try:
    n = int(input('Enter a number:\n'))
    
    while i * i <= n:
        if n % i == 0:
            print(str(n) + ' is not a prime')
            
        else:
            print(str(n) + ' is a prime')
            break
        i = i + 1
except Exception as details:
    print('Not a number')

except ValueError as details:
    print('Not a number')

finally:
    print()

