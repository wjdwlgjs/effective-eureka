from sys import stdin, setrecursionlimit
from collections import deque

setrecursionlimit(100001)
n = int(stdin.readline())

out_adjlist = [deque() for _ in range(n+1)]
in_adjlist = [deque() for _ in range(n+1)]
input_list = [None] + list(map(int, stdin.readline().split()))

for i in range(1, n+1):
    if i - input_list[i] > 0:
        out_adjlist[i].append(i - input_list[i])
        in_adjlist[i - input_list[i]].append(i)
    if i + input_list[i] <= n:
        out_adjlist[i].append(i + input_list[i])
        in_adjlist[i + input_list[i]].append(i)

visit_id = [-1 for _ in range(n+1)]
which_scc = [-1 for _ in range(n+1)]
cur_scc = 0
cur_visit = 0
stack = deque()
sccs = []
sccs_counts = []


def dfs(cur_node):
    global cur_visit, cur_scc
    if which_scc[cur_node] != -1:
        return 2147483647
    if visit_id[cur_node] != -1:
        return visit_id[cur_node]
    
    visit_id[cur_node] = cur_visit
    return_value = cur_visit
    cur_visit += 1
    stack.append(cur_node)

    for adjnode in out_adjlist[cur_node]:
        return_value = min(return_value, dfs(adjnode))
    
    if return_value == visit_id[cur_node]:
        temp = -1
        sccs.append(deque())
        sccs_counts.append(0)
        while temp != cur_node:
            temp = stack.pop()
            sccs[cur_scc].append(temp)
            which_scc[temp] = cur_scc
        cur_scc += 1

    return return_value

s = int(stdin.readline())
dfs(s)

for i in range(cur_scc - 1, -1, -1):
    for scc_element in sccs[i]:
        for prev_node in in_adjlist[scc_element]:
            if which_scc[prev_node] != which_scc[scc_element]:
                sccs_counts[i] = max(sccs_counts[i], sccs_counts[which_scc[prev_node]])
    sccs_counts[i] += len(sccs[i])

print(max(sccs_counts))