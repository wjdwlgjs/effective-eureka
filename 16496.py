from sys import stdin
from functools import cmp_to_key

n = int(stdin.readline())
input_list = stdin.readline().split()

def list_to_int(_list: list):
    return_str = ""
    for element in _list:
        return_str += element
    return int(return_str)

def compare(a:str, b:str):
    return int(b + a) - int(a + b)

input_list.sort(key=cmp_to_key(compare))
print(list_to_int(input_list))