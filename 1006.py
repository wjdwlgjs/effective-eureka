from sys import stdin

INF = 2147483647
T = int(stdin.readline())
add_list = (2, 1, 1, 0, 1)
valid_prev_list = [(0, 1, 2, 3, 4), (0, 2), (0, 1), (0,), (0, 1, 2, 3, 4)]

for _ in range(T):
    n, w = map(int,stdin.readline().split())
    input_list = [list(map(int, stdin.readline().split())) for __ in range(2)]
    min_count = INF
    
    for i in range(5):
        if input_list[0][0] + input_list[0][-1] > w and (i == 1 or i == 3):
            continue
        elif input_list[1][0] + input_list[1][-1] > w and (i == 2 or i == 3):
            continue
        elif i == 4 and input_list[0][0] + input_list[1][0] > w:
            continue
        
        dp_list = [[0 for __ in range(n)] for ___ in range(5)]
        for j in range(5):
            if i != j:
                dp_list[j][0] = INF
            else:
                dp_list[j][0] = add_list[i]
        
        for j in range(1, n):
            for k in range(5):
                dp_list[k][j] = min(dp_list[l][j-1] for l in valid_prev_list[k]) + add_list[k]

            if input_list[0][j-1] + input_list[0][j] > w:
                dp_list[1][j] = INF
                dp_list[3][j] = INF
            if input_list[1][j-1] + input_list[1][j] > w:
                dp_list[2][j] = INF
                dp_list[3][j] = INF
            if input_list[0][j] + input_list[1][j] > w:
                dp_list[4][j] = INF
        min_count = min(min_count, min(dp_list[l][-1] for l in valid_prev_list[i]))
    
    
    print(min_count)



