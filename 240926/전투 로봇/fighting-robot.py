from collections import deque

N = int(input())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

ROBOT_LV = 2
MONSTER_CNT = 0
MONSTERS_LEVEL = []
KILLED_MONSTER = 0 # 레벨업 확인용

for i in range(N):
    for j in range(N):
        if MATRIX[i][j] == 9:
            ROBOT_X = i
            ROBOT_Y = j
        elif 0 < MATRIX[i][j] < 7:
            MONSTER_CNT += 1
            MONSTERS_LEVEL.append(MATRIX[i][j])

TIME = 0


# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 죽일 몬스터의 위치로 최소한의 거리로 이동
# (tx, ty)는 죽일 몬스터의 좌표(= 목표점)
# (x, y)는 현재 좌표
# cnt는 현재까지 이동 거리
# bfs로 바꿔보자
MIN_DIS = 400
TARGET_X = -1
TARGET_Y = -1
def move(start_x, start_y):
    global MIN_DIS, TARGET_X, TARGET_Y

    q = deque([[start_x, start_y, 0]]) # 세번째인자는 이동거리

    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[start_x][start_y] = True

    while q:
        x, y, dis = q.popleft()

        if 0 < MATRIX[x][y] < 7 and MATRIX[x][y] < ROBOT_LV:
            if dis < MIN_DIS:
                MIN_DIS = dis
                TARGET_X = x
                TARGET_Y = y
            elif dis == MIN_DIS:
                if x < TARGET_X:
                    TARGET_X = x
                    TARGET_Y = y
                elif x == TARGET_X:
                    if y < TARGET_Y:
                        TARGET_X = x
                        TARGET_Y = y

        if dis > MIN_DIS:
            break

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if -1 < nx < N and -1 < ny < N and not visited[nx][ny] and MATRIX[nx][ny] <= ROBOT_LV:
                q.append([nx, ny, dis+1])
                visited[nx][ny] = True



while MONSTER_CNT != 0:
# for i in range(20):
    print()
    if min(MONSTERS_LEVEL) >= ROBOT_LV:
        break
    MIN_DIS = 400
    move(ROBOT_X, ROBOT_Y)
    if MIN_DIS == 400: # 그럼 이동 못한 거
        break
    else:
        TIME += MIN_DIS
        MONSTERS_LEVEL.remove(MATRIX[TARGET_X][TARGET_Y])
        MATRIX[ROBOT_X][ROBOT_Y] = 0
        ROBOT_X, ROBOT_Y = TARGET_X, TARGET_Y
        MATRIX[ROBOT_X][ROBOT_Y] = 9
        KILLED_MONSTER += 1
        MONSTER_CNT -= 1
        if KILLED_MONSTER == ROBOT_LV:
            ROBOT_LV += 1
            KILLED_MONSTER = 0

print(TIME)