N = int(input())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

ROBOT_LV = 2
for i in range(N):
    for j in range(N):
        if MATRIX[i][j] == 9:
            ROBOT_X = i
            ROBOT_Y = j


TIME = 0


# 죽일 몬스터 위치 탐색 - 만약 얘가 -1을 리턴한다면 죽일 수 있는 게 없다는 뜻
# 무조건 0,0부터 아니고 현 위치에서 젤 가까운 거 해야 함. 결국 힙쳐ㅑ 더ㅐ
# def who_kill():
#     res = -1
#     for i in range(N):
#         for j in range(N):
#             if 0 < MATRIX[i][j] < ROBOT_LV:
#                 res = [i, j]
#                 return res
#     return res


# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 죽일 몬스터의 위치로 최소한의 거리로 이동
# (tx, ty)는 죽일 몬스터의 좌표(= 목표점)
# (x, y)는 현재 좌표
# cnt는 현재까지 이동 거리
MIN_DIS = 400
TARGET_X = -1
TARGET_Y = -1
def move(x, y, cnt, visited):
    global MIN_DIS, TARGET_X, TARGET_Y

    if 0 < MATRIX[x][y] < ROBOT_LV:
        if cnt < MIN_DIS:
            MIN_DIS = cnt
            TARGET_X = x
            TARGET_Y = y
        elif cnt == MIN_DIS:
            if x < TARGET_X:
                TARGET_X = x
                TARGET_Y = y
            elif x == TARGET_X:
                if y < TARGET_Y:
                    TARGET_X = x
                    TARGET_Y = y
        return

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if -1 < nx < N and -1 < ny < N and not visited[nx][ny] and MATRIX[nx][ny] <= ROBOT_LV:
            visited[nx][ny] = True
            move(nx, ny, cnt+1, visited)
            visited[nx][ny] = False


def update_min_dis():
    global MIN_DIS
    MIN_DIS = 400


KILLED_MONSTER = 0
while True:
    VISITED = [[False for _ in range(N)] for _ in range(N)]
    update_min_dis()
    VISITED[ROBOT_X][ROBOT_Y] = True
    move(ROBOT_X, ROBOT_Y, 0, VISITED)
    if MIN_DIS == 400: # 그럼 이동 못한 거
        break
    else:
        # print('여기로 이동했어', TARGET_X, TARGET_Y, MIN_DIS)
        TIME += MIN_DIS
        MATRIX[ROBOT_X][ROBOT_Y] = 0
        ROBOT_X, ROBOT_Y = TARGET_X, TARGET_Y
        MATRIX[ROBOT_X][ROBOT_Y] = 9
        KILLED_MONSTER += 1
        if KILLED_MONSTER == ROBOT_LV:
            ROBOT_LV += 1
            KILLED_MONSTER = 0

print(TIME)
# 문제: DFS가 제대로 안 돌고 있음. 그래서 MIN_DIS 가 갱신이 안 된다.