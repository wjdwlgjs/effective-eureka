from sys import stdin, setrecursionlimit
from collections import deque

n, m = map(int, stdin.readline().split())

setrecursionlimit(max(n, 1000))
roots = [i for i in range(n+1)]
queue = deque()

def find_root(cur_id):
    if cur_id != roots[cur_id]:
        roots[cur_id] = find_root(roots[cur_id])
    return roots[cur_id]

for _ in range(m):
    query, a, b = map(int, stdin.readline().split())

    if query == 0:
        a = find_root(a)
        b = find_root(b)
        roots[max(a, b)] = min(a, b)
    
    else:
        if find_root(a) == find_root(b):
            print('YES')
        else:
            print('NO')
