from copy import deepcopy

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
def who_kill():
    res = -1
    for i in range(N):
        for j in range(N):
            if 0 < MATRIX[i][j] < ROBOT_LV:
                res = [i, j]
                return res
    return res


# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 죽일 몬스터의 위치로 최소한의 거리로 이동
# (tx, ty)는 죽일 몬스터의 좌표(= 목표점)
# (x, y)는 현재 좌표
# cnt는 현재까지 이동 거리
MIN_DIS = 400
def move(x, y, tx, ty, cnt, visited):
    global MIN_DIS

    if x == tx and y == ty:
        MIN_DIS = cnt if cnt < MIN_DIS else MIN_DIS
        return

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if -1 < nx < N and -1 < ny < N and not visited[nx][ny] and MATRIX[nx][ny] <= ROBOT_LV:
            new_visited = deepcopy(visited)
            new_visited[nx][ny] = True
            move(nx, ny, tx, ty, cnt+1, new_visited)


def update_min_dis():
    global MIN_DIS
    MIN_DIS = 400

# VISITED = [[False for _ in range(N)] for _ in range(N)]
# while True:
#     target_pos = who_kill()
#     if target_pos == -1:
#         break
#     MIN_DIS = 400
#     move(ROBOT_X, ROBOT_Y, target_pos[0], target_pos[1], 0, VISITED) # 마지막엔 로봇도 이동해야 함
#     TIME += MIN_DIS
#     MATRIX[ROBOT_X][ROBOT_Y] = 0
#     ROBOT_X, ROBOT_Y = target_pos[0], target_pos[1]
#     MATRIX[ROBOT_X][ROBOT_Y] = 9


KILLED_MONSTER = 0
while True:
    VISITED = [[False for _ in range(N)] for _ in range(N)]
    VISITED[ROBOT_X][ROBOT_Y] = True
    target_pos = who_kill()
    if target_pos == -1:
        break
    else:
        # MIN_DIS 초기화
        update_min_dis()
#         # 아 이게 종료조건 말고 걍 for문으로 끝날수도 있어서 무조건 MIN_DIS가 갱신된다고 여기면 안돼
#         # 죽일 몬은 있는데 이동이 아예 불가능할수도 있어
        move(ROBOT_X, ROBOT_Y, target_pos[0], target_pos[1], 0, VISITED)
        # print('MIN_DIS', MIN_DIS)
        if MIN_DIS == 400: # 그럼 이동 못한 거
            break
        else:
            TIME += MIN_DIS
            MATRIX[ROBOT_X][ROBOT_Y] = 0
            ROBOT_X, ROBOT_Y = target_pos[0], target_pos[1]
            MATRIX[ROBOT_X][ROBOT_Y] = 9
            KILLED_MONSTER += 1
            if KILLED_MONSTER == ROBOT_LV:
                ROBOT_LV += 1
                KILLED_MONSTER = 0
            # print(TIME)

print(TIME)
# 문제: DFS가 제대로 안 돌고 있음. 그래서 MIN_DIS 가 갱신이 안 된다.