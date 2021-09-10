#!/usr/bin/python3

import random

total = 0

for i in range(0, 100):
    n = random.randrange(0,99)
    total += n
    print(str(n) + " ")

print('\n')
print('Average is ' + str(total/100)) 

    
