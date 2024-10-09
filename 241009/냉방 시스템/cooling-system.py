N, M, K = map(int, input().split())
AIR_COND_INFO = [] # (x, y, d)
OFFICE = []

MATRIX = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        if MATRIX[i][j] >= 2:
            AIR_COND_INFO.append((i, j, MATRIX[i][j]%4))
        elif MATRIX[i][j] == 1:
            OFFICE.append((i, j))


WIND = [[0 for _ in range(N)] for _ in range(N)] # 바람의 양

WALL = [[[] for _ in range(N)] for _ in range(N)]
for i in range(M): # 이때 d는 0(위에 벽), 1(왼쪽 벽) 뿐임
    x, y, d = map(int, input().split())
    WALL[x-1][y-1].append(d)

# d: 우하좌상 0123 or 4523 (방향 d == d%4)
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

from collections import deque

q = deque()

def wind_right(air_x, air_y):
    global WIND
    air_d = 0
    fx, fy = air_x+dx[air_d], air_y+dy[air_d]
    if not in_range(fx, fy):
        return
    WIND[fx][fy] += 5

    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[fx][fy] = True

    q.append((fx, fy, 5))
    while q:
        x, y, wind_cnt = q.popleft()
        if wind_cnt == 0:
            break
        # 45도 위(위->오)
        # 검사할 벽: 내자리 위쪽에 벽이 있는가, x-1 y+1 자리 왼쪽에 벽이 있는가
        if in_range(x-1, y) and in_range(x-1, y+1) and not visited[x-1][y+1] and (0 not in  WALL[x][y]) and (1 not in WALL[x-1][y+1]):
            WIND[x-1][y+1] += wind_cnt-1
            q.append((x-1, y+1, wind_cnt-1))
            visited[x-1][y+1] = True
        # 직진
        # 검사할 벽: x, y+1 자리 왼쪽에 벽이 있는가
        if in_range(x, y+1) and not visited[x][y+1] and (1 not in WALL[x][y+1]):
            WIND[x][y+1] += wind_cnt-1
            q.append((x, y+1, wind_cnt-1))
            visited[x][y+1] = True
        # 45도 아래(아래->오)
        # 검사할 벽: x+1, y 위쪽에 벽이 있는가, x+1 y+1 자리 왼쪽에 벽이 있는가
        if in_range(x+1, y) and in_range(x+1, y+1) and not visited[x+1][y+1] and (0 not in WALL[x+1][y]) and (1 not in WALL[x+1][y+1]):
            WIND[x+1][y+1] += wind_cnt-1
            q.append((x+1, y+1, wind_cnt-1))
            visited[x+1][y+1] = True


def wind_left(air_x, air_y):
    global WIND
    air_d = 2
    fx, fy = air_x+dx[air_d], air_y+dy[air_d]
    if not in_range(fx, fy):
        return
    WIND[fx][fy] += 5

    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[fx][fy] = True
    
    q.append((fx, fy, 5))
    while q:
        x, y, wind_cnt = q.popleft()
        if wind_cnt == 0:
            break
        # 45도 위(위->왼)
        # 검사할 벽: 내자리 위쪽에 벽이 있는가, x-1, y 자리 왼쪽에 벽이 있는가
        if in_range(x-1, y) and in_range(x-1, y-1) and not visited[x-1][y-1] and (0 not in  WALL[x][y]) and (1 not in WALL[x-1][y]):
            WIND[x-1][y-1] += wind_cnt-1
            q.append((x-1, y-1, wind_cnt-1))
            visited[x-1][y-1] = True
        # 직진
        # 검사할 벽: 내자리 왼쪽에 벽이 있는가
        if in_range(x, y-1) and not visited[x][y-1] and (1 not in WALL[x][y]):
            WIND[x][y-1] += wind_cnt-1
            q.append((x, y-1, wind_cnt-1))
            visited[x][y-1] = True
        # 45도 아래(아래->왼)
        # 검사할 벽: x+1, y 위쪽에 벽이 있는가, x+1 y 자리 왼쪽에 벽이 있는가
        if in_range(x+1, y) and in_range(x+1, y-1) and not visited[x+1][y-1] and (0 not in WALL[x+1][y]) and (1 not in WALL[x+1][y]):
            WIND[x+1][y-1] += wind_cnt-1
            q.append((x+1, y-1, wind_cnt-1))
            visited[x+1][y-1] = True


def wind_up(air_x, air_y):
    global WIND
    air_d = 3
    fx, fy = air_x+dx[air_d], air_y+dy[air_d]
    if not in_range(fx, fy):
        return
    WIND[fx][fy] += 5

    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[fx][fy] = True

    q.append((fx, fy, 5))
    while q:
        x, y, wind_cnt = q.popleft()
        if wind_cnt == 0:
            break
        # 45도 왼(왼->위)
        # 검사할 벽: 내자리 왼쪽에 벽이 있는가, x, y-1 자리 위쪽에 벽이 있는가
        if in_range(x, y-1) and in_range(x-1, y-1) and not visited[x-1][y-1] and (1 not in  WALL[x][y]) and (0 not in WALL[x][y-1]):
            WIND[x-1][y-1] += wind_cnt-1
            q.append((x-1, y-1, wind_cnt-1))
            visited[x-1][y-1] = True
        # 직진
        # 검사할 벽: 내자리 위쪽에 벽이 있는가
        if in_range(x-1, y) and not visited[x-1][y] and (0 not in WALL[x][y]):
            WIND[x-1][y] += wind_cnt-1
            q.append((x-1, y, wind_cnt-1))
            visited[x-1][y] = True
        # 45도 우(오->위)
        # 검사할 벽: x, y+1 왼쪽에 벽이 있는가, x, y+1 자리 위쪽에 벽이 있는가
        if in_range(x, y+1) and in_range(x-1, y+1) and not visited[x-1][y+1] and (0 not in WALL[x][y+1]) and (1 not in WALL[x][y+1]):
            WIND[x-1][y+1] += wind_cnt-1
            q.append((x-1, y+1, wind_cnt-1))
            visited[x-1][y+1] = True


def wind_down(air_x, air_y):
    global WIND
    air_d = 1
    fx, fy = air_x+dx[air_d], air_y+dy[air_d]
    if not in_range(fx, fy):
        return
    WIND[fx][fy] += 5

    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[fx][fy] = True

    q.append((fx, fy, 5))
    while q:
        x, y, wind_cnt = q.popleft()
        if wind_cnt == 0:
            break
        # 45도 왼(왼->아래)
        # 검사할 벽: 내자리 왼쪽에 벽이 있는가, x+1, y-1 자리 위쪽에 벽이 있는가
        if in_range(x, y-1) and in_range(x+1, y-1) and not visited[x+1][y-1] and (1 not in  WALL[x][y]) and (0 not in WALL[x+1][y-1]):
            WIND[x+1][y-1] += wind_cnt-1
            q.append((x+1, y-1, wind_cnt-1))
            visited[x+1][y-1] = True
        # 직진
        # 검사할 벽: x+1, y 위쪽에 벽이 있는가
        if in_range(x+1, y) and not visited[x+1][y] and (0 not in WALL[x+1][y]):
            WIND[x+1][y] += wind_cnt-1
            q.append((x+1, y, wind_cnt-1))
            visited[x+1][y] = True
        # 45도 우(오->아래)
        # 검사할 벽: x, y+1 왼쪽에 벽이 있는가, x+1, y+1 자리 위쪽에 벽이 있는가
        if in_range(x, y+1) and in_range(x+1, y+1) and not visited[x-1][y+1] and (1 not in WALL[x][y+1]) and (0 not in WALL[x+1][y+1]):
            WIND[x+1][y+1] += wind_cnt-1
            q.append((x+1, y+1, wind_cnt-1))
            visited[x+1][y+1] = True


def air_cond_work():
    global WIND

    # 에어컨들이 순서대로 동작하면서 바람의 양을 갱신
    for ax, ay, ad in AIR_COND_INFO:
        # visited = [[False for _ in range(N)] for _ in range(N)]
        if ad == 0: # 바람방향: 오른쪽
            wind_right(ax, ay)
        elif ad == 1: # 바람방향: 아래쪽
            wind_down(ax, ay)
        elif ad == 2: # 바람방향: 왼쪽
            wind_left(ax, ay)
        elif ad == 3: # 바람방향: 위쪽
            wind_up(ax, ay)


def mix_air():
    global WIND

    new_matrix = [[0 for _ in range(N)] for _ in range(N)]
    
    # 상하좌우: 3120
    for x in range(N):
        for y in range(N):
            if WIND[x][y] > 0:
                # 위쪽
                upx, upy = x+dx[3], y+dy[3]
                if in_range(upx, upy) and (0 not in WALL[x][y]) and WIND[x][y] > WIND[upx][upy]:
                    dist = (WIND[x][y] - WIND[upx][upy]) // 4
                    new_matrix[x][y] -= dist
                    new_matrix[upx][upy] += dist
                # 아래쪽
                downx, downy = x+dx[1], y+dy[1]
                if in_range(downx, downy) and (0 not in WALL[x+1][y]) and WIND[x][y] > WIND[downx][downy]:
                    dist = (WIND[x][y] - WIND[downx][downy]) // 4
                    new_matrix[x][y] -= dist
                    new_matrix[downx][downy] += dist
                # 왼쪽
                leftx, lefty = x+dx[2], y+dy[2]
                if in_range(leftx, lefty) and (1 not in WALL[x][y]) and WIND[x][y] > WIND[leftx][lefty]:
                    dist = (WIND[x][y] - WIND[leftx][lefty]) // 4
                    new_matrix[x][y] -= dist
                    new_matrix[leftx][lefty] += dist
                # 오른쪽
                rightx, righty = x+dx[0], y+dy[0]
                if in_range(rightx, righty) and (1 not in WALL[x][y+1]) and WIND[x][y] > WIND[rightx][righty]:
                    dist = (WIND[x][y] - WIND[rightx][righty]) // 4
                    new_matrix[x][y] -= dist
                    new_matrix[rightx][righty] += dist

    for i in range(N):
        for j in range(N):
            WIND[i][j] += new_matrix[i][j]


for minutes in range(1, 101):
    if minutes == 100:
        minutes = -1
        break
    # print(' ===== ', minutes, '분 ===== ')
    # print('이동 전')
    # for _ in WIND:
    #     print(_)
    # print()
    ''' 1. 에어컨 작동 '''
    air_cond_work()
    # print('이동 후')
    # for _ in WIND:
    #     print(_)
    # print()

    ''' 2. 공기 섞임 '''
    mix_air()
    # print('섞인 후')
    # for _ in WIND:
    #     print(_)
    # print()
    ''' 3. 외벽칸 시원함 1 감소 '''
    # 맨 위, 맨 아래
    for i in range(N):
        if WIND[0][i] != 0:
            WIND[0][i] -= 1
        if WIND[N-1][i] != 0:
            WIND[N-1][i] -= 1
    # 맨 왼, 맨 오
    for j in range(1, N-1):
        if WIND[j][0] != 0:
            WIND[j][0] -= 1
        if WIND[j][N-1] != 0:
            WIND[j][N-1] -= 1
    ''' 모든 사무실 시원한 정도가 K이상이면 break '''
    ALL_COOL = True
    for x, y in OFFICE:
        if WIND[x][y] < K:
            ALL_COOL = False
            # if minutes >= 16:
            #     print('작아요', WIND[x][y], x, y)
            break
    
    # print('외벽 감소 후')
    # for _ in WIND:
    #     print(_)
    # print()

    # if minutes >= 16:
    #     for _ in WIND:
    #         print(_)
    #     print()

    if ALL_COOL:
        break

print(minutes)