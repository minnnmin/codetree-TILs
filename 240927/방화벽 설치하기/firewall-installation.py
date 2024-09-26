from copy import deepcopy
from collections import deque

N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

FIRES = [] # 불 위치
for i in range(N):
    for j in range(M):
        if MATRIX[i][j] == 2:
            FIRES.append([i, j])


MAX_NO_FIRE_CNT = 0


# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


# (x, y)가 범위 안에 있냐
def in_range(x, y):
    return -1 < x < N and -1 < y < M


# 불 안 번진 곳 개수 세서 MAX_NO_FIRE_CNT 변수 갱신
def update_max_no_fire_cnt(new_matrix):
    global MAX_NO_FIRE_CNT

    res = 0
    for i in range(N):
        for j in range(M):
            if new_matrix[i][j] == 0:
                res += 1

    if res > MAX_NO_FIRE_CNT:
        MAX_NO_FIRE_CNT = res


# bfs
def fire_spread(start_x, start_y, now_matrix):
    q = deque([[start_x, start_y]])
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if in_range(nx, ny) and now_matrix[nx][ny] == 0:
                q.append([nx, ny])
                now_matrix[nx][ny] = 2
                

# back tracking
def add_3_firewalls(ex_i, ex_j, n):
    if n == 3:
        new_matrix = deepcopy(MATRIX) # 이거 왜 되냐...
        for x, y in FIRES:
            fire_spread(x, y, new_matrix)
        update_max_no_fire_cnt(new_matrix)
        return

    for i in range(ex_i, N):
        for j in range(ex_j+1, M):
            if MATRIX[i][j] == 0:
                MATRIX[i][j] = 1
                add_3_firewalls(i, j, n+1)
                MATRIX[i][j] = 0

add_3_firewalls(-1, -1, 0)
print(MAX_NO_FIRE_CNT)