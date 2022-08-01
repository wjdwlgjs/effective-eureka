from sys import stdin

n = int(stdin.readline())
input_list = []
length = 0

for _ in range(n):
    x, y = map(int, stdin.readline().split())
    input_list.append([x, y])

input_list.sort()

cur_range = input_list[0]

for temp_range in input_list[1:]:
    if temp_range[0] > cur_range[1]:
        length += cur_range[1] - cur_range[0]
        cur_range = temp_range
    else:
        cur_range[1] = max(cur_range[1], temp_range[1])

length += cur_range[1] - cur_range[0]

print(length)