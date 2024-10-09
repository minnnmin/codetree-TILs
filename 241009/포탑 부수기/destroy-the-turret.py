N, M, K = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]
BROKEN = [[0 for _ in range(M)] for _ in range(N)]
LATEST_ATTACK_TURN = [[0 for _ in range(M)] for _ in range(N)]

for i in range(N):
    for j in range(M):
        if MATRIX[i][j] == 0:
            BROKEN[i][j] = 1


# 오른쪽부터 시계방향으로
dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]


def in_range(x, y):
    return -1 < x < N and -1 < y < M

def fix_pos(x, y):
    if x < 0:
        x = x+N
    elif x >= N:
        x = x%N
    if y < 0:
        y = y+M
    elif y >= M:
        y = y%M
    return x, y

from collections import deque

q = deque()

# 공격위치, 타겟 위치
def laser_attack(x, y, tx, ty):

    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[x][y] = True
    q.append((x, y, 0, [None])) # 마지막 인자는 이때까지 지나온 방향
    move_history = [] # 이동 방향이 들어감!
    dis_to_target = 1e9
    CAN_ATTACK = False

    while q:
        x, y, dis, history = q.popleft()
        if (x, y) == (tx, ty):
            if dis < dis_to_target or (dis == dis_to_target and history < move_history):
                # history.pop()
                move_history = history
                dis_to_target = dis
                CAN_ATTACK = True
        else:
            for i in range(0, 8, 2): # 상하좌우만 검사
                nx, ny = x+dx[i], y+dy[i]
                nx, ny = fix_pos(nx, ny)
                if not BROKEN[nx][ny] and not visited[nx][ny]:
                    q.append((nx, ny, dis+1, history + [i]))
                    visited[nx][ny] = True

    return CAN_ATTACK, move_history


for turn in range(1, K+1):
    ''' 1. 공격할 포탑 선택 '''
    attack_related = [[0 for _ in range(M)] for _ in range(N)]
    min_power = 5001
    min_pos = (-1, -1)
    latest_attack_turn = -1
    for i in range(N):
        for j in range(M):
            if BROKEN[i][j]:
                continue
            if MATRIX[i][j] < min_power or (MATRIX[i][j] == min_power and latest_attack_turn < LATEST_ATTACK_TURN[i][j]) or\
                (MATRIX[i][j] == min_power and latest_attack_turn == LATEST_ATTACK_TURN[i][j] and sum(min_pos) < i+j) or\
                (MATRIX[i][j] == min_power and latest_attack_turn == LATEST_ATTACK_TURN[i][j] and sum(min_pos) == i+j and min_pos[1] < j):
                min_power = MATRIX[i][j]
                min_pos = (i, j)
                latest_attack_turn = LATEST_ATTACK_TURN[i][j]
    LATEST_ATTACK_TURN[min_pos[0]][min_pos[1]] = turn # 최근 공격한 턴 정보 갱신
    MATRIX[min_pos[0]][min_pos[1]] += N + M
    attack_related[min_pos[0]][min_pos[1]] = 1
    # print('공격자', min_pos, min_power, MATRIX[min_pos[0]][min_pos[1]])
    ''' 2. 공격자 포탑의 공격 '''
    # 공격대상 선택
    max_power = 0
    max_pos = (N, N)
    latest_attack_turn = K+1
    for i in range(N):
        for j in range(M):
            if BROKEN[i][j] or (i, j) == min_pos:
                continue
            if MATRIX[i][j] > max_power or (MATRIX[i][j] == max_power and latest_attack_turn > LATEST_ATTACK_TURN[i][j]) or\
                (MATRIX[i][j] == max_power and latest_attack_turn == LATEST_ATTACK_TURN[i][j] and sum(max_pos) > i+j) or\
                (MATRIX[i][j] == max_power and latest_attack_turn == LATEST_ATTACK_TURN[i][j] and sum(max_pos) == i+j and max_pos[1] > j):
                max_power = MATRIX[i][j]
                max_pos = (i, j)
                latest_attack_turn = LATEST_ATTACK_TURN[i][j]
    # print('타겟', max_pos, max_power)
    # === 공격 ===
    # bfs 돌려서 목적지에 닿을 수 있다면 공격 가능 (이때 지나온 좌표 모두 기억)
    CAN_ATTACK, move_history = laser_attack(min_pos[0], min_pos[1], max_pos[0], max_pos[1])
    # print(CAN_ATTACK)
    # print('공격 전')
    # for _ in MATRIX:
    #     print(_)
    if CAN_ATTACK: # 레이저 공격 실행
        # print('레이저')
        x, y = min_pos[0], min_pos[1]
        power = MATRIX[x][y]
        # 목표 포탑 공격
        MATRIX[max_pos[0]][max_pos[1]] -= power
        attack_related[max_pos[0]][max_pos[1]] = 1
        if MATRIX[max_pos[0]][max_pos[1]] <= 0:
            BROKEN[max_pos[0]][max_pos[1]] = 1
        move_history.pop()
        # print(move_history)
        # 지나온 애들도 공격
        for d in move_history[1:]:
            x, y = x+dx[d], y+dy[d]
            x, y = fix_pos(x, y)
            MATRIX[x][y] -= power//2
            attack_related[x][y] = 1
            if MATRIX[x][y] <= 0:
                BROKEN[x][y] = 1
    else: # 포탄 공격 실행
        # print('포탄')
        x, y = min_pos[0], min_pos[1]
        power = MATRIX[x][y]
        # 목표 포탑 공격
        mx, my = max_pos[0], max_pos[1]
        MATRIX[mx][my] -= power
        if MATRIX[max_pos[0]][max_pos[1]] <= 0:
            BROKEN[max_pos[0]][max_pos[1]] = 1
        attack_related[max_pos[0]][max_pos[1]] = 1
        # 주위 8방향 애들도 공격
        for i in range(8):
            mmx, mmy = mx+dx[i], my+dy[i]
            mmx, mmy = fix_pos(mmx, mmy)
            if not BROKEN[mmx][mmy]:
                MATRIX[mmx][mmy] -= power//2
                attack_related[mmx][mmy] = 1
                if MATRIX[mmx][mmy] <= 0:
                    BROKEN[mmx][mmy] = 1
    # print('공격 후')
    # for _ in MATRIX:
    #     print(_)
    ''' 포탑 하나 남으면 즉시 종료 '''
    survive_num = 0
    for i in range(N):
        for j in range(M):
            if not BROKEN[i][j]:
                survive_num += 1
            if survive_num > 1:
                break
    if survive_num == 1:
        # print('설마?')
        break
    ''' 공격과 무관한 포탑 +1 '''
    for i in range(N):
        for j in range(M):
            if not BROKEN[i][j] and not attack_related[i][j]:
                MATRIX[i][j] += 1
    # print('재정비 후')
    # for _ in MATRIX:
    #     print(_)

# 남아 있는 가장 강한 포탑의 공격력 출력
ANSWER = 0
for i in range(N):
    for j in range(M):
        if not BROKEN[i][j] and MATRIX[i][j] > ANSWER:
            ANSWER = MATRIX[i][j]
print(ANSWER)