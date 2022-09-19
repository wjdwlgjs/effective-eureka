from sys import stdin
from functools import cmp_to_key

n = int(stdin.readline())
m = int(stdin.readline())

input_lines = []
maxroundend = 0
minroundstart = n+1

for i in range(1, m+1):
    start, end = map(int, stdin.readline().split())
    if start < end:
        input_lines.append([start, end, i])
    else:
        input_lines.append([start, end, i])
        maxroundend = max(maxroundend, end)
        minroundstart = min(minroundstart, start)

lines = []
validness = [True for _ in range(m+1)]

for i in input_lines:
    if validness[i[2]]:
        if i[0] < i[1] and (i[1] <= maxroundend or i[0] >= minroundstart):
            validness[i[2]] = False
        elif i[0] > i[1]:
            i[1] += n
            lines.append(i)
        else:
            lines.append(i)

def compare(a, b):
    if a[0] != b[0]:
        return a[0] - b[0]
    else:
        return b[1] - a[1]

lines.sort(key = cmp_to_key(compare))


for i in range(1, len(lines)):
    if lines[i][0] == lines[i-1][0]:
        lines[i][1] = lines[i-1][1]
        validness[lines[i][2]] = False
    elif lines[i][1] <= lines[i-1][1]:
        lines[i][0] = lines[i -1][0]
        lines[i][1] = lines[i-1][1]
        validness[lines[i][2]] = False

for i in range(1, m+1):
    if validness[i]:
        print(i, end = " ")
