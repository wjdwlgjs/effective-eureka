from sys import stdin
from functools import cmp_to_key

n = int(stdin.readline())
input_list = stdin.readline().split()

def compare(a:str, b:str):
    if int(b + a) > int(a + b):
        return 1
    else:
        return -1

input_list.sort(key = cmp_to_key(compare))
for i in input_list:
    print(i, end = "")