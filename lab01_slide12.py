#!/usr/bin/python3

import random

n = 0
rand = random.randrange(10)

while n >= 0 and n <= 9:
    n = int(input('Enter a number between 0-9:\n'))
    if n == rand:
        print('Correct') 
        break
    else:
        print('Guess Again!')
