from sys import stdin, setrecursionlimit
from collections import deque

setrecursionlimit(100001)
n, m = map(int, stdin.readline().split())

children_from_id = [deque() for _ in range(n+1)]
visit_from_id = [-1 for _ in range(n+1)]
id_from_visit = [-1]
starts = [-1 for _ in range(n+1)]
ends = [-1 for _ in range(n+1)]

parent_id_from_id = [None] + list(map(int, stdin.readline().split()))

for i in range(2, n+1):
    children_from_id[parent_id_from_id[i]].append(i)

segtree = [0 for _ in range(n * 4 + 1)] # sum_from_visit 
lazytree = [0 for _ in range(n * 4 + 1)]

def edit(start, end, goal_start, goal_end, tree_idx, val):
    if lazytree[tree_idx] != 0:
        segtree[tree_idx] += lazytree[tree_idx] * (end - start + 1)
        if start != end:
            lazytree[tree_idx * 2] += lazytree[tree_idx]
            lazytree[tree_idx * 2 + 1] += lazytree[tree_idx]
        lazytree[tree_idx] = 0
    
    if start > goal_end or end < goal_start:
        return 0
    
    if start >= goal_start and end <= goal_end:
        segtree[tree_idx] += val * (end - start + 1)
        if start != end:
            lazytree[tree_idx * 2] += val
            lazytree[tree_idx * 2 + 1] += val
        return segtree[tree_idx]
    
    mid = (start + end) // 2

    segtree[tree_idx] = edit(start, mid, goal_start, goal_end, tree_idx * 2, val) + edit(mid + 1, end, goal_start, goal_end, tree_idx * 2 + 1, val)
    return segtree[tree_idx]

def get(start, end, goal_start, goal_end, tree_idx):
    if start > goal_end or end < goal_start:
        return 0
    
    if lazytree[tree_idx] != 0:
        segtree[tree_idx] += lazytree[tree_idx] * (end - start + 1)
        if start != end:
            lazytree[tree_idx * 2] += lazytree[tree_idx]
            lazytree[tree_idx * 2 + 1] += lazytree[tree_idx]
        lazytree[tree_idx] = 0
    
    if start >= goal_start and end <= goal_end:
        return segtree[tree_idx]
    
    mid = (start + end) // 2
    return get(start, mid, goal_start, goal_end, tree_idx * 2) + get(mid + 1, end, goal_start, goal_end, tree_idx * 2 + 1)

dfs_call_count = 0
def dfs(cur_id):
    global dfs_call_count
    dfs_call_count += 1
    starts[cur_id] = dfs_call_count
    id_from_visit.append(cur_id)

    for i in children_from_id[cur_id]:
        dfs(i)

    ends[cur_id] = dfs_call_count

dfs(1)

for _ in range(m):
    query = list(map(int, stdin.readline().split()))
    if query[0] == 1:
        edit(1, n, starts[query[1]], ends[query[1]], 1, query[2])
    
    else:
        print(get(1, n, starts[query[1]], starts[query[1]], 1))