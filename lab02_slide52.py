#!/usr/bin/python3

def tally(string):
    t = {}
    for ch in string:
        if ch in t:
            t[ch] += 1
        else:
            t[ch] = 1

    max = 0
    result = ''
    for ch in t:
        #print(ch, t[ch])
        if t[ch] > max:
            max = t[ch]
            result = ch
    #print(max)
    print(result)


print('Enter a string:')
tally(input())
