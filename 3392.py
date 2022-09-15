from sys  import stdin
from functools import cmp_to_key

total = 0
max_ceiling = [0 for _ in range(120001)]
min_ceiling = [0 for _ in range(120001)]
need_propagation = [False for _ in range(120001)]

def add(start, end, goal_start, goal_end, floor, ceiling, tree_idx):
    global total
    if ceiling <= min_ceiling[tree_idx]:
        return
    # print('before', start, '~', end, " min", min_ceiling[tree_idx], "max", max_ceiling[tree_idx], 'propagate', need_propagation[tree_idx])
    if need_propagation[tree_idx] and start != end:
        max_ceiling[tree_idx*2] = max_ceiling[tree_idx]
        max_ceiling[tree_idx*2+1] = max_ceiling[tree_idx]
        min_ceiling[tree_idx*2] = min_ceiling[tree_idx]
        min_ceiling[tree_idx*2+1] = min_ceiling[tree_idx]
        need_propagation[tree_idx*2] = True
        need_propagation[tree_idx*2+1] = True
        need_propagation[tree_idx] = False
        # print("propagated", start, "~", end, "max", max_ceiling[tree_idx], "min", min_ceiling[tree_idx])
    
    if start == goal_start and end == goal_end:
        if max_ceiling[tree_idx] < floor:
            total += (ceiling - floor + 1) * (end - start + 1)
            # print(start, "~", end, "added", (ceiling - floor + 1) * (end - start + 1))
            max_ceiling[tree_idx] = ceiling
            min_ceiling[tree_idx] = ceiling
            need_propagation[tree_idx] = True
        elif max_ceiling[tree_idx] == min_ceiling[tree_idx]:
            total += (ceiling - max_ceiling[tree_idx]) * (end - start + 1)
            # print(start, "~", end, "added", (ceiling - max_ceiling[tree_idx]) * (end - start + 1), '1')
            max_ceiling[tree_idx] = ceiling
            min_ceiling[tree_idx] = ceiling
            need_propagation[tree_idx] = True
        else:
            mid = (start + end) // 2
            if mid >= goal_start:
                add(start, mid, goal_start, min(goal_end, mid), floor, ceiling, tree_idx * 2)
            if mid + 1 <= goal_end:
                add(mid+1, end, max(mid+1, goal_start), goal_end, floor, ceiling, tree_idx*2+1)
            min_ceiling[tree_idx] = min(min_ceiling[tree_idx*2], min_ceiling[tree_idx*2+1])
            max_ceiling[tree_idx] = max(max_ceiling[tree_idx*2], max_ceiling[tree_idx*2+1])
    
    else:
        mid = (start + end) // 2
        if mid >= goal_start:
            add(start, mid, goal_start, min(goal_end, mid), floor, ceiling, tree_idx*2)
        if mid +1 <= goal_end:
            add(mid+1, end, max(goal_start, mid+1), goal_end, floor, ceiling, tree_idx*2+1)
        min_ceiling[tree_idx] = min(min_ceiling[tree_idx*2], min_ceiling[tree_idx*2+1])
        max_ceiling[tree_idx] = max(max_ceiling[tree_idx*2], max_ceiling[tree_idx*2+1])
    
    # print(start, '~', end, " min", min_ceiling[tree_idx], "max", max_ceiling[tree_idx], 'propagate', need_propagation[tree_idx])
n = int(stdin.readline())

def compare(a, b):
    return a[1] - b[1]

input_list = [tuple(map(int, stdin.readline().split())) for _ in range(n)]
input_list.sort(key = cmp_to_key(compare))
for x1, y1, x2, y2 in input_list:
    add(1, 30000, x1+1, x2, y1+1, y2, 1)
    # print()


print(total)
