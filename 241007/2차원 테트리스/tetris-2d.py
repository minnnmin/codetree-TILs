# 게임 맵
MATRIX = [[0 for _ in range(10)] for _ in range(10)]
for i in range(4, 10):
    for j in range(4, 10):
        MATRIX[i][j] = -1


K = int(input())
ORDER = [list(map(int, input().split())) for _ in range(K)]
SCORE = 0

def in_range(x, y):
    return -1 < x < 10 and -1 < y < 10

def move_block(t, x, y):
    global MATRIX
    if t == 1:
        # yellow
        for i in range(4, 11):
            if not in_range(i, y) or MATRIX[i][y] != 0:
                MATRIX[i-1][y] = 1
                break
        # red
        for j in range(4, 11):
            if not in_range(x, j) or MATRIX[x][j] != 0:
                MATRIX[x][j-1] = 1
                break
    elif t == 2:
        # yellow
        for i in range(4, 11):
            if not in_range(i, y) or MATRIX[i][y] != 0 or MATRIX[i][y+1] != 0:
                MATRIX[i-1][y], MATRIX[i-1][y+1] = 1, 1
                break
        # red
        for j in range(4, 11):
            if not in_range(x, j+1) or MATRIX[x][j] != 0 or MATRIX[x][j+1] != 0:
                MATRIX[x][j-1], MATRIX[x][j] = 1, 1
                break
    elif t == 3:
        # yellow
        for i in range(4, 11):
            if not in_range(i+1, y) or MATRIX[i][y] != 0 or MATRIX[i+1][y] != 0:
                MATRIX[i-1][y], MATRIX[i][y] = 1, 1
                break
        # red
        for j in range(4, 11):
            if not in_range(x, j) or MATRIX[x][j] != 0 or MATRIX[x+1][j] != 0:
                MATRIX[x][j-1], MATRIX[x+1][j-1] = 1, 1
                break


def check_game():
    global MATRIX, SCORE

    deleted_row = []
    deleted_col = []

    # yellow 검사
    for row in range(9, 5, -1):
        if (MATRIX[row][0], MATRIX[row][1], MATRIX[row][2], MATRIX[row][3]) == (1, 1, 1, 1):
            deleted_row.append(row)
            MATRIX[row][0], MATRIX[row][1], MATRIX[row][2], MATRIX[row][3] = 0, 0, 0, 0
            SCORE += 1
    
    if deleted_row:
        # yellow 블럭 땡기기
        del_cnt = 0
        for row in range(deleted_row[0], 1, -1):
            if row in deleted_row:
                del_cnt += 1
            else:
                MATRIX[row+del_cnt][0], MATRIX[row+del_cnt][1], MATRIX[row+del_cnt][2], MATRIX[row+del_cnt][3] =\
                    MATRIX[row][0], MATRIX[row][1], MATRIX[row][2], MATRIX[row][3]
        
    # red 검사
    for col in range(9, 5, -1):
        if (MATRIX[0][col], MATRIX[1][col], MATRIX[2][col], MATRIX[3][col]) == (1, 1, 1, 1):
            deleted_col.append(col)
            MATRIX[0][col], MATRIX[1][col], MATRIX[2][col], MATRIX[3][col] = 0, 0, 0, 0
            SCORE += 1

    if deleted_col:
        # red 블럭 땡기기
        del_cnt = 0
        for col in range(deleted_col[0], 1, -1):
            if col in deleted_col:
                del_cnt += 1
            else:
                MATRIX[0][col+del_cnt], MATRIX[1][col+del_cnt], MATRIX[2][col+del_cnt], MATRIX[3][col+del_cnt] =\
                    MATRIX[0][col], MATRIX[1][col], MATRIX[2][col], MATRIX[3][col]



def check_overflow():
    global MATRIX

    # yellow overflow
    # 1. 4행도 초과 -> 2칸 이동
    if sum(MATRIX[4][:4]) > 0:
        for row in range(7, 1, -1):
            MATRIX[row+2][0], MATRIX[row+2][1], MATRIX[row+2][2], MATRIX[row+2][3] =\
                MATRIX[row][0], MATRIX[row][1], MATRIX[row][2], MATRIX[row][3]
    # 2. 5행만 초과 -> 1칸 이동
    elif sum(MATRIX[5][:4]) > 0:
        for row in range(8, 2, -1):
            MATRIX[row+1][0], MATRIX[row+1][1], MATRIX[row+1][2], MATRIX[row+1][3] =\
                MATRIX[row][0], MATRIX[row][1], MATRIX[row][2], MATRIX[row][3]

    # red overflow
    # 1. 4열도 초과 -> 2칸 이동
    if MATRIX[0][4] + MATRIX[1][4] + MATRIX[2][4] + MATRIX[3][4] > 0:
        for col in range(7, 1, -1):
            MATRIX[0][col+2], MATRIX[1][col+2], MATRIX[2][col+2], MATRIX[3][col+2] =\
                MATRIX[0][col], MATRIX[1][col], MATRIX[2][col], MATRIX[3][col]
    # 2. 5열만 초과 -> 1칸 이동
    elif MATRIX[0][5] + MATRIX[1][5] + MATRIX[2][5] + MATRIX[3][5] > 0:
        for col in range(8, 2, -1):
            MATRIX[0][col+1], MATRIX[1][col+1], MATRIX[2][col+1], MATRIX[3][col+1] =\
                MATRIX[0][col], MATRIX[1][col], MATRIX[2][col], MATRIX[3][col]



for turn, (t, x, y) in enumerate(ORDER):
    move_block(t, x, y)
    # print('이동 후')
    # for _ in MATRIX:
    #     print(_)
    # print()
    check_game()
    # print('한줄 차서 처리한 후')
    # for _ in MATRIX:
    #     print(_)
    # print()
    check_overflow()
    # print('오버플로우 처리 후')
    # for _ in MATRIX:
    #     print(_)
    # print()
    # print(t, x, y)
    # for _ in MATRIX:
    #     print(_)

cnt = 0
for i in range(10):
    for j in range(10):
        if MATRIX[i][j] == 1:
            cnt += 1
print(SCORE)
print(cnt)