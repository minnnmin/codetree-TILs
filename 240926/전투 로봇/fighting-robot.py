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
MIN_DIS = 400
TARGET_X = -1
TARGET_Y = -1
def move(x, y, cnt, visited):
    global MIN_DIS, TARGET_X, TARGET_Y

    if cnt > MIN_DIS:
        return

    if 0 < MATRIX[x][y] < 7 and 0 < MATRIX[x][y] < ROBOT_LV:
        # print('hi')
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
    
    # 남은 것들 못 먹는데, 싹다 돌 때 

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if -1 < nx < N and -1 < ny < N and not visited[nx][ny] and MATRIX[nx][ny] <= ROBOT_LV:
            visited[nx][ny] = True
            move(nx, ny, cnt+1, visited)
            visited[nx][ny] = False



# while MONSTER_CNT != 0:
#     VISITED = [[False for _ in range(N)] for _ in range(N)]
#     update_min_dis()
#     VISITED[ROBOT_X][ROBOT_Y] = True
#     move(ROBOT_X, ROBOT_Y, 0, VISITED)
#     if MIN_DIS == 1e9: # 그럼 이동 못한 거
#         print('이동 못해')
#         break
#     else:
#         print('여기로 이동했어', TARGET_X, TARGET_Y, MIN_DIS)
#         TIME += MIN_DIS
#         MATRIX[ROBOT_X][ROBOT_Y] = 0
#         ROBOT_X, ROBOT_Y = TARGET_X, TARGET_Y
#         MATRIX[ROBOT_X][ROBOT_Y] = 9
#         for _ in MATRIX:
#             print(_)
#         KILLED_MONSTER += 1
#         MONSTER_CNT -= 1
#         if KILLED_MONSTER == ROBOT_LV:
#             ROBOT_LV += 1
#             KILLED_MONSTER = 0

# print(TIME)


while MONSTER_CNT != 0:
    if min(MONSTERS_LEVEL) >= ROBOT_LV:
        break
    VISITED = [[False for _ in range(N)] for _ in range(N)]
    # update_min_dis()
    MIN_DIS = 400
    VISITED[ROBOT_X][ROBOT_Y] = True
    move(ROBOT_X, ROBOT_Y, 0, VISITED)
    if MIN_DIS == 400: # 그럼 이동 못한 거
        # print('이동 못해')
        break
    else:
        TIME += MIN_DIS
        MONSTERS_LEVEL.remove(MATRIX[TARGET_X][TARGET_Y])
        MATRIX[ROBOT_X][ROBOT_Y] = 0
        ROBOT_X, ROBOT_Y = TARGET_X, TARGET_Y
        MATRIX[ROBOT_X][ROBOT_Y] = 9
        # print('여기로 이동했어', TARGET_X, TARGET_Y, MIN_DIS, TIME, ROBOT_LV, i)
        # for _ in MATRIX:
        #     print(_)
        KILLED_MONSTER += 1
        MONSTER_CNT -= 1
        if KILLED_MONSTER == ROBOT_LV:
            ROBOT_LV += 1
            KILLED_MONSTER = 0

print(TIME)