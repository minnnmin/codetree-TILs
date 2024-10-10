import heapq

R, C, K = map(int, input().split())
R, C = R-1, C-1
MATRIX = [[0 for _ in range(100)] for _ in range(100)]

for i in range(3):
    a, b, c = map(int, input().split())
    MATRIX[i][0], MATRIX[i][1], MATRIX[i][2] = a, b, c

ROW_CNT = 3
COL_CNT = 3


# 힙 용도
h = []


def row_sort():
    global MATRIX, COL_CNT

    for row in range(100):
        count = {} # num: cnt
        for num in MATRIX[row]:
            if num == 0:
                continue
            if num in count:
                count[num] += 1
            else:
                count[num] = 1
        # print()
        # print('row', row)
        # print('count', count)
        for num, cnt in count.items():
            heapq.heappush(h, (cnt, num)) # 빈도 작은 게 먼저
        # print('h', h)
        i = 0
        while h:
            cnt, num = heapq.heappop(h)
            # print(cnt, num)
            MATRIX[row][i], MATRIX[row][i+1] = num, cnt
            i += 2
        if i > COL_CNT:
            COL_CNT = i
        for col in range(i, 100):
            MATRIX[row][col] = 0
        # print('while문 탈출')
        # print(i)
        # print(MATRIX[row])


def col_sort():
    global MATRIX, ROW_CNT

    for col in range(100):
        count = {} # num: cnt
        for row in range(100):
            num = MATRIX[row][col]
            if num == 0:
                continue
            if num in count:
                count[num] += 1
            else:
                count[num] = 1
        for num, cnt in count.items():
            heapq.heappush(h, (cnt, num)) # 빈도 작은 게 먼저
        i = 0
        while h:
            cnt, num = heapq.heappop(h)
            MATRIX[i][col], MATRIX[i+1][col] = num, cnt
            i += 2
        if i > ROW_CNT:
            ROW_CNT = i
        for row in range(i, 100):
            MATRIX[row][col] = 0


if MATRIX[R][C] == K:
    print(0)
else:
    FIND = False
    for sec in range(1, 101):
        ''' 행이 크면 행, 열이 크면 열을 정렬 '''
        if ROW_CNT >= COL_CNT:
            row_sort()
        else:
            col_sort()
            # for r in range(10):
            #     for c in range(10):
            #         print(MATRIX[r][c], end=' ')
            #     print()
        ''' 만약 MATRIX[R][C] == K 면 break '''
        if MATRIX[R][C] == K:
            FIND = True
            break
    if FIND:
        print(sec)
    else:
        print(-1)