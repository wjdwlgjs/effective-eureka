from sys import stdin
from functools import cmp_to_key

n = int(stdin.readline())
roots = [i for i in range(n)]
positions_by_x = []
positions_by_y = []
posititons_by_z = []

for i in range(n):
    input_tuple = tuple(map(int, [i] + stdin.readline().split()))
    positions_by_x.append(input_tuple)
    positions_by_y.append(input_tuple)
    posititons_by_z.append(input_tuple)

#[cost, node, node]
edges = []

def compare_position(a, b):
    return a[pos] - b[pos]

pos = 1
positions_by_x.sort(key = cmp_to_key(compare_position))
pos = 2
positions_by_y.sort(key = cmp_to_key(compare_position))
pos = 3
posititons_by_z.sort(key = cmp_to_key(compare_position))

for i in range(n-1):
    node0 = positions_by_x[i]
    node1 = positions_by_x[i+1]
    cost = abs(node0[1] - node1[1])
    edges.append((cost, node0[0], node1[0]))
    node0 = positions_by_y[i]
    node1 = positions_by_y[i+1]
    cost = abs(node0[2] - node1[2])
    edges.append((cost, node0[0], node1[0]))
    node0 = posititons_by_z[i]
    node1 = posititons_by_z[i+1]
    cost = abs(node0[3] - node1[3])
    edges.append((cost, node0[0], node1[0]))

edges.sort()

valid_edge_count = 0
total_cost = 0

def find_root(cur_id):
    if cur_id != roots[cur_id]:
        roots[cur_id] = find_root(roots[cur_id])
    return roots[cur_id]

for cost, node0, node1 in edges:
    temp_root0 = find_root(node0)
    temp_root1 = find_root(node1)

    if temp_root0 != temp_root1:
        valid_edge_count += 1
        total_cost += cost

        roots[max(temp_root0, temp_root1)] = min(temp_root0, temp_root1)
    
    if valid_edge_count == n-1:
        break

print(total_cost)

