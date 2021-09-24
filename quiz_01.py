#!/usr/bin/python3

s = input('Enter a string:\n')
try:
    i = int(input('Enter an interval:\n'))

    while i < 0:
        i = int(input('Interval must be positive'))

except Exception as details:
    print(str(details))
except ValueError as details:
    print(str(details))
finally:
    print()



for index in range(0, len(s)):
    if index == 0:
        print(s[index])
    elif index % i == 0:
        print(s[index])



