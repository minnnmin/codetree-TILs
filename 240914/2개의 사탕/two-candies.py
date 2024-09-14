from copy import copy, deepcopy

N, M = map(int, input().split())

matrix = []
for _ in range(N):
    matrix.append(list(input()))

for i in range(N):
    for j in range(M):
        if matrix[i][j] == 'R':
            RED = [i, j]
        elif matrix[i][j] == 'B':
            BLUE = [i, j]
        elif matrix[i][j] == 'O':
            EXIT = [i, j]

min_cnt = 20

def dfs(now_matrix, ex_directions, cnt, RED, BLUE):
    global min_cnt, EXIT
    # 종료조건
    if cnt > 10:
        return
    if BLUE == EXIT:
        return
    if RED == EXIT and BLUE != EXIT and cnt <= 10:
        min_cnt = min(min_cnt, cnt)
        return
    
    if ex_directions[-1] == 'L':
        martix1 = deepcopy(now_matrix)
        martix2 = deepcopy(now_matrix)
        RED1 = copy(RED)
        BLUE1 = copy(BLUE)
        RED2 = copy(RED)
        BLUE2 = copy(BLUE)
        martix1, RED1, BLUE1 = make_new_matrix(matrix1, 'U', RED1, BLUE1)
        dfs(martix1, ex_directions + ['U'], cnt + 1, RED1, BLUE1)
        martix2, RED2, BLUE2 = make_new_matrix(martix2, 'D', RED2, BLUE2)
        dfs(martix2, ex_directions + ['D'], cnt + 1, RED2, BLUE2)

    elif ex_directions[-1] == 'R':
        martix3 = deepcopy(now_matrix)
        martix4 = deepcopy(now_matrix)
        RED3 = copy(RED)
        BLUE3 = copy(BLUE)
        RED4 = copy(RED)
        BLUE4 = copy(BLUE)
        martix3, RED3, BLUE3 = make_new_matrix(martix3, 'U', RED3, BLUE3)
        dfs(martix3, ex_directions + ['U'], cnt + 1, RED3, BLUE3)
        martix4, RED4, BLUE4 = make_new_matrix(martix4, 'D', RED4, BLUE4)
        dfs(martix4, ex_directions + ['D'], cnt + 1, RED4, BLUE4)

    elif ex_directions[-1] == 'U':
        martix5 = deepcopy(now_matrix)
        martix6 = deepcopy(now_matrix)
        RED5 = copy(RED)
        BLUE5 = copy(BLUE)
        RED6 = copy(RED)
        BLUE6 = copy(BLUE)
        martix5, RED5, BLUE5 = make_new_matrix(martix5, 'L', RED5, BLUE5)
        dfs(martix5, ex_directions + ['L'], cnt + 1, RED5, BLUE5)
        martix6, RED6, BLUE6 = make_new_matrix(martix6, 'R', RED6, BLUE6)
        dfs(martix6, ex_directions + ['R'], cnt + 1, RED6, BLUE6)
            
    elif ex_directions[-1] == 'D':
        martix7 = deepcopy(now_matrix)
        martix8 = deepcopy(now_matrix)
        RED7 = copy(RED)
        BLUE7 = copy(BLUE)
        RED8 = copy(RED)
        BLUE8 = copy(BLUE)
        martix7, RED7, BLUE7 = make_new_matrix(martix7, 'L', RED7, BLUE7)
        dfs(martix7, ex_directions + ['L'], cnt + 1, RED7, BLUE7)
        martix8, RED8, BLUE8 = make_new_matrix(martix8, 'R', RED8, BLUE8)
        dfs(martix8, ex_directions + ['R'], cnt + 1, RED8, BLUE8)

def make_new_matrix(now_matrix, direction, RED, BLUE):
    if direction == 'L': # 단, 블루가 레드 왼쪽에 있으면 먼저 가야 함
        if RED[0] == BLUE[0]:
            if RED[1] < BLUE[1]:
                for _ in range(M-3):
                    if now_matrix[RED[0]][RED[1] - 1] == '.':
                        now_matrix[RED[0]][RED[1] - 1] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] -= 1
                    elif now_matrix[RED[0]][RED[1] - 1] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] -= 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[BLUE[0]][BLUE[1] - 1] == '.':
                        now_matrix[BLUE[0]][BLUE[1] - 1] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] -= 1
                    elif now_matrix[BLUE[0]][BLUE[1] - 1] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] -= 1
                        break
                    else:
                        break
            else:
                for _ in range(M-3):
                    if now_matrix[BLUE[0]][BLUE[1] - 1] == '.':
                        now_matrix[BLUE[0]][BLUE[1] - 1] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] -= 1
                    elif now_matrix[BLUE[0]][BLUE[1] - 1] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] -= 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[RED[0]][RED[1] - 1] == '.':
                        now_matrix[RED[0]][RED[1] - 1] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] -= 1
                    elif now_matrix[RED[0]][RED[1] - 1] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] -= 1
                        break
                    else:
                        break
        else: # 아무거나 먼저 해
            for _ in range(M-3):
                if now_matrix[RED[0]][RED[1] - 1] == '.':
                    now_matrix[RED[0]][RED[1] - 1] = 'R'
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[1] -= 1
                elif now_matrix[RED[0]][RED[1] - 1] == 'O':
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[1] -= 1
                    break
                else:
                    break
            for _ in range(M-3):
                if now_matrix[BLUE[0]][BLUE[1] - 1] == '.':
                    now_matrix[BLUE[0]][BLUE[1] - 1] = 'B'
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[1] -= 1
                elif now_matrix[BLUE[0]][BLUE[1] - 1] == 'O':
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[1] -= 1
                    break
                else:
                    break
        return now_matrix, RED, BLUE

    elif direction == 'R':
        if RED[0] == BLUE[0]:
            if RED[1] < BLUE[1]:
                for _ in range(M-3):
                    if now_matrix[BLUE[0]][BLUE[1] + 1] == '.':
                        now_matrix[BLUE[0]][BLUE[1] + 1] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] += 1
                    elif now_matrix[BLUE[0]][BLUE[1] + 1] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] += 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[RED[0]][RED[1] + 1] == '.':
                        now_matrix[RED[0]][RED[1] + 1] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] += 1
                    elif now_matrix[RED[0]][RED[1] + 1] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] += 1
                        break
                    else:
                        break
            else:
                for _ in range(M-3):
                    if now_matrix[RED[0]][RED[1] + 1] == '.':
                        now_matrix[RED[0]][RED[1] + 1] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] += 1
                    elif now_matrix[RED[0]][RED[1] + 1] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[1] += 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[BLUE[0]][BLUE[1] + 1] == '.':
                        now_matrix[BLUE[0]][BLUE[1] + 1] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] += 1
                    elif now_matrix[BLUE[0]][BLUE[1] + 1] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[1] += 1
                        break
                    else:
                        break
        else: # 아무거나 먼저 해
            for _ in range(M-3):
                if now_matrix[RED[0]][RED[1] + 1] == '.':
                    now_matrix[RED[0]][RED[1] + 1] = 'R'
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[1] += 1
                elif now_matrix[RED[0]][RED[1] + 1] == 'O':
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[1] += 1
                    break
                else:
                    break
            for _ in range(M-3):
                if now_matrix[BLUE[0]][BLUE[1] + 1] == '.':
                    now_matrix[BLUE[0]][BLUE[1] + 1] = 'B'
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[1] += 1
                elif now_matrix[BLUE[0]][BLUE[1] + 1] == 'O':
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[1] += 1
                    break
                else:
                    break
        return now_matrix, RED, BLUE

    elif direction == 'U':
        if RED[1] == BLUE[1]:
            if RED[0] < BLUE[0]:
                for _ in range(N-3):
                    if now_matrix[RED[0] - 1][RED[1]] == '.':
                        now_matrix[RED[0] - 1][RED[1]] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] -= 1
                    elif now_matrix[RED[0] - 1][RED[1]] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] -= 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[BLUE[0] - 1][BLUE[1]] == '.':
                        now_matrix[BLUE[0] - 1][BLUE[1]] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] -= 1
                    elif now_matrix[BLUE[0] - 1][BLUE[1]] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] -= 1
                        break
                    else:
                        break
            else:
                for _ in range(M-3):
                    if now_matrix[BLUE[0] - 1][BLUE[1]] == '.':
                        now_matrix[BLUE[0] - 1][BLUE[1]] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] -= 1
                    elif now_matrix[BLUE[0] - 1][BLUE[1]] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] -= 1
                        break
                    else:
                        break
                for _ in range(N-3):
                    if now_matrix[RED[0] - 1][RED[1]] == '.':
                        now_matrix[RED[0] - 1][RED[1]] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] -= 1
                    elif now_matrix[RED[0] - 1][RED[1]] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] -= 1
                        break
                    else:
                        break
        else: # 아무거나 먼저 해
            for _ in range(M-3):
                if now_matrix[RED[0] - 1][RED[1]] == '.':
                    now_matrix[RED[0] - 1][RED[1]] = 'R'
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[0] -= 1
                elif now_matrix[RED[0] - 1][RED[1]] == 'O':
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[0] -= 1
                    break
                else:
                    break
            for _ in range(M-3):
                if now_matrix[BLUE[0] - 1][BLUE[1]] == '.':
                    now_matrix[BLUE[0] - 1][BLUE[1]] = 'B'
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[0] -= 1
                elif now_matrix[BLUE[0] - 1][BLUE[1]] == 'O':
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[0] -= 1
                    break
                else:
                    break
        return now_matrix, RED, BLUE

    elif direction == 'D':
        if RED[1] == BLUE[1]:
            if RED[0] < BLUE[0]:
                for _ in range(M-3):
                    if now_matrix[BLUE[0] + 1][BLUE[1]] == '.':
                        now_matrix[BLUE[0] + 1][BLUE[1]] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] += 1
                    elif now_matrix[BLUE[0] + 1][BLUE[1]] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] += 1
                        break
                    else:
                        break
                for _ in range(N-3):
                    if now_matrix[RED[0] + 1][RED[1]] == '.':
                        now_matrix[RED[0] + 1][RED[1]] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] += 1
                    elif now_matrix[RED[0] + 1][RED[1]] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] += 1
                        break
                    else:
                        break
            else:
                for _ in range(N-3):
                    if now_matrix[RED[0] + 1][RED[1]] == '.':
                        now_matrix[RED[0] + 1][RED[1]] = 'R'
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] += 1
                    elif now_matrix[RED[0] + 1][RED[1]] == 'O':
                        now_matrix[RED[0]][RED[1]] = '.'
                        RED[0] += 1
                        break
                    else:
                        break
                for _ in range(M-3):
                    if now_matrix[BLUE[0] + 1][BLUE[1]] == '.':
                        now_matrix[BLUE[0] + 1][BLUE[1]] = 'B'
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] += 1
                    elif now_matrix[BLUE[0] + 1][BLUE[1]] == 'O':
                        now_matrix[BLUE[0]][BLUE[1]] = '.'
                        BLUE[0] += 1
                        break
                    else:
                        break
        else: # 아무거나 먼저 해
            for _ in range(N-3):
                if now_matrix[RED[0] + 1][RED[1]] == '.':
                    now_matrix[RED[0] + 1][RED[1]] = 'R'
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[0] += 1
                elif now_matrix[RED[0] + 1][RED[1]] == 'O':
                    now_matrix[RED[0]][RED[1]] = '.'
                    RED[0] += 1
                    break
                else:
                    break
            for _ in range(M-3):
                if now_matrix[BLUE[0] + 1][BLUE[1]] == '.':
                    now_matrix[BLUE[0] + 1][BLUE[1]] = 'B'
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[0] += 1
                elif now_matrix[BLUE[0] + 1][BLUE[1]] == 'O':
                    now_matrix[BLUE[0]][BLUE[1]] = '.'
                    BLUE[0] += 1
                    break
                else:
                    break
        return now_matrix, RED, BLUE

matrix1 = deepcopy(matrix)
matrix2 = deepcopy(matrix)
matrix3 = deepcopy(matrix)
matrix4 = deepcopy(matrix)
RED1 = copy(RED)
BLUE1 = copy(BLUE)
RED2 = copy(RED)
BLUE2 = copy(BLUE)
RED3 = copy(RED)
BLUE3 = copy(BLUE)
RED4 = copy(RED)
BLUE4 = copy(BLUE)

matrix_L, RED1, BLUE1 = make_new_matrix(matrix1, 'L', RED1, BLUE1)
dfs(matrix_L, ['L'], 1, RED1, BLUE1)
matrix_R, RED2, BLUE2 = make_new_matrix(matrix2, 'R', RED2, BLUE2)
dfs(matrix_R, ['R'], 1, RED2, BLUE2)
matrix_U, RED3, BLUE3 = make_new_matrix(matrix3, 'U', RED3, BLUE3)
dfs(matrix_U, ['U'], 1, RED3, BLUE3)
matrix_D, RED4, BLUE4 = make_new_matrix(matrix4, 'D', RED4, BLUE4)
dfs(matrix_D, ['D'], 1, RED4, BLUE4)

if min_cnt == 20:
    print(-1)
else:
    print(min_cnt)