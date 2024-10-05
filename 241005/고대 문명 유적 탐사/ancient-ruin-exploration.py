from copy import deepcopy

K, M = map(int, input().split())

MATRIX = [list(map(int, input().split())) for _ in range(5)]
WALL_NUMS = list(map(int, input().split()))
WALL_POINTER = 0


# (x, y) 중심으로 해서 3x3 크기 배열을 시계 방향 90도 회전 - 카피 매트릭스 대상
def rotate_fake(x, y):
    global COPY_MATRIX # rotate 호출 전 MATRIX 카피 해서 써야 함
    TMP_MATRIX = [[0 for _ in range(5)] for _ in range(5)]
    
    # 위 -> 오른쪽
    for i, j in zip(range(x+1, x-2, -1), range(y+1, y-2, -1)):
        TMP_MATRIX[i][y+1] = COPY_MATRIX[x-1][j]
    # 왼쪽 -> 위
    for i, j in zip(range(x-1, x+2), range(y+1, y-2, -1)):
        TMP_MATRIX[x-1][j] = COPY_MATRIX[i][y-1]
    # 아래 -> 왼쪽
    for i, j in zip(range(x-1, x+2), range(y-1, y+2)):
        TMP_MATRIX[i][y-1] = COPY_MATRIX[x+1][j]
    # 오른쪽 -> 아래
    for i, j in zip(range(x-1, x+2), range(y+1, y-2, -1)):
        TMP_MATRIX[x+1][j] = COPY_MATRIX[i][y+1]
    # 가운데
    TMP_MATRIX[x][y] = COPY_MATRIX[x][y]
    # 마지막에 tmp를 matrix에 옮겨
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            COPY_MATRIX[i][j] = TMP_MATRIX[i][j]


# # 만들어진 COPY_MATRIX를 가지고 얻을 수 있는 유물 가치를 리턴
# def get_value(): # bfs
#     pass


# (x, y) 중심으로 해서 3x3 크기 배열을 시계 방향 90만큼 회전 - 리얼 매트릭스 대상
def rotate_real(x, y):
    global MATRIX
    TMP_MATRIX = [[0 for _ in range(5)] for _ in range(5)]

    # 위 -> 오른쪽
    for i, j in zip(range(x+1, x-2, -1), range(y+1, y-2, -1)):
        TMP_MATRIX[i][y+1] = MATRIX[x-1][j]
    # 왼쪽 -> 위
    for i, j in zip(range(x-1, x+2), range(y+1, y-2, -1)):
        TMP_MATRIX[x-1][j] = MATRIX[i][y-1]
    # 아래 -> 왼쪽
    for i, j in zip(range(x-1, x+2), range(y-1, y+2)):
        TMP_MATRIX[i][y-1] = MATRIX[x+1][j]
    # 오른쪽 -> 아래
    for i, j in zip(range(x-1, x+2), range(y+1, y-2, -1)):
        TMP_MATRIX[x+1][j] = MATRIX[i][y+1]
    # 가운데
    TMP_MATRIX[x][y] = MATRIX[x][y]
    # 마지막에 tmp를 matrix에 옮겨
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            MATRIX[i][j] = TMP_MATRIX[i][j]


from collections import deque
q = deque()

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < 5 and -1 < y < 5

# (x, y)에 대해 bfs - 인접한 동일 조각의 개수를 리턴. 이 리턴값이 3 이상이어야 유의미한 것
def bfs(x, y):
    global visited

    target = COPY_MATRIX[x][y]
    visited[x][y] = True
    q.append((x, y))
    cnt = 1

    while q:
        r, c = q.popleft()
        for i in range(4):
            nr, nc = r+dx[i], c+dy[i]
            if in_range(nr, nc) and not visited[nr][nc] and COPY_MATRIX[nr][nc] == target:
                visited[nr][nc] = True
                q.append((nr, nc))
                cnt += 1
    return cnt


# 찐 MATRIX 가지고 돌면서 이번에는 history에 좌표들 저장, MATRIX에서 삭제된 곳 0으로 바꿔
def bfs_real(x, y):
    global visited, MATRIX

    target = MATRIX[x][y]
    visited[x][y] = True
    q.append((x, y))
    cnt = 1
    history = [(x, y)]

    while q:
        r, c = q.popleft()
        for i in range(4):
            nr, nc = r+dx[i], c+dy[i]
            if in_range(nr, nc) and not visited[nr][nc] and MATRIX[nr][nc] == target:
                visited[nr][nc] = True
                q.append((nr, nc))
                history.append((nr, nc))
                cnt += 1
    # if cnt >= 3:
        # print('bfs 안, 중심과 history', x, y, history)
    return cnt, history


for turn in range(K):
    ANSWER = 0 # 유물 가치의 총합
    '''=== 1. 탐사 진행 ==='''
    # 총 9개의 중심에 대해 90, 180, 270도 회전을 해보면서
    # 유물 획득 가치가 최대인(회전각도 작은, 중심의 열이 작은, 행이 작은) 경우를 세팅
    MAX_VAL = -1
    CENTER_POS = (-1, -1)
    ANGLE = -1
    for y in range(1, 4):
        for x in range(1, 4):
            # (x, y)가 회전의 중심
            # COPY_MATRIX를 회전하면서 최대 가치 창줄하는 중심과 회전각도 얻어내기
            COPY_MATRIX = deepcopy(MATRIX)

            # 90도
            rotate_fake(x, y)
            res90 = 0
            visited = [[False for _ in range(5)] for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    if not visited[i][j]:
                        cnt = bfs(i, j)
                        if cnt >= 3:
                            res90 += cnt
            if res90 > MAX_VAL or (res90 == MAX_VAL and ANGLE > 90):
                MAX_VAL = res90
                CENTER_POS = (x, y)
                ANGLE = 90
            
            # 180도
            rotate_fake(x, y)
            res180 = 0
            visited = [[False for _ in range(5)] for _ in range(5)]            
            for i in range(5):
                for j in range(5):
                    if not visited[i][j]:
                        cnt = bfs(i, j)
                        if cnt >= 3:
                            res180 += cnt
            if res180 > MAX_VAL or (res180 == MAX_VAL and ANGLE > 180):
                MAX_VAL = res180
                CENTER_POS = (x, y)
                ANGLE = 180

            # 270도
            rotate_fake(x, y)
            res270 = 0
            visited = [[False for _ in range(5)] for _ in range(5)]            
            for i in range(5):
                for j in range(5):
                    if not visited[i][j]:
                        cnt = bfs(i, j)
                        if cnt >= 3:
                            res270 += cnt
            if res270 > MAX_VAL:
                MAX_VAL = res270
                CENTER_POS = (x, y)
                ANGLE = 270

    # print('정해진 중심좌표:', CENTER_POS)
    # print('정해진 각도:', ANGLE)
    
    # 자 이제 회전 중심(CENTER_POS)과 각도(ANGLE)가 정해졌으니
    # 실제로 MATRIX를 회전시킨 다음 유물을 획득해 본다.
    if ANGLE == 90:
        rotate_real(CENTER_POS[0], CENTER_POS[1])
    elif ANGLE == 180:
        rotate_real(CENTER_POS[0], CENTER_POS[1])
        rotate_real(CENTER_POS[0], CENTER_POS[1])
    elif ANGLE == 270:
        rotate_real(CENTER_POS[0], CENTER_POS[1])
        rotate_real(CENTER_POS[0], CENTER_POS[1])
        rotate_real(CENTER_POS[0], CENTER_POS[1])

    '''=== 2. 유물 획득 ==='''
    answer = 0
    while 1:
        visited = [[False for _ in range(5)] for _ in range(5)]
        deleted_pos = []
        for i in range(5):
            for j in range(5):
                if not visited[i][j]:
                    cnt, history = bfs_real(i, j)
                    if cnt >= 3:
                        answer += cnt
                        deleted_pos += history
        if len(deleted_pos) == 0:
            # print('삭제될 게 없어요')
            break
        for i, j in deleted_pos:
            MATRIX[i][j] = 0
        deleted_pos.sort(key = lambda x : (x[1], -x[0]))
        for dr, dc in deleted_pos:
            MATRIX[dr][dc] = WALL_NUMS[WALL_POINTER]
            WALL_POINTER += 1
    if answer != 0:
        print(answer, end = ' ')
    else:
        break