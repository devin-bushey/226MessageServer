#!/usr/bin/python3

s = input('Enter a string:\n')
result = ""

for i in range(0, len(s)):
    if (i + 1) % 3 == 0:
        result = result + s[i]

print(result)


