N, M, BATTERY = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

for i in range(N):
    for j in range(N):
        if MATRIX[i][j] == 1:
            MATRIX[i][j] = 'WALL'

tx, ty = map(int, input().split())
CAR_POS = (tx-1, ty-1)

# 태우고 나면
FINISHED = [False for _ in range(M+1)]

# 승객 위치, 목적지 위치 - 0번째 안씀
PASSENGER_POS = [0, ]
PASSENGER_DEST = [0, ]
for i in range(M):
    x, y, x2, y2 = map(int, input().split())
    PASSENGER_POS.append((x-1, y-1))
    PASSENGER_DEST.append((x2-1, y2-1))
    MATRIX[x-1][y-1] = i+1 # 승객번호 저장

# print(MATRIX)
# print(PASSENGER_POS)
# print(PASSENGER_DEST)

# 상우하좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

from collections import deque

q = deque()

def get_min_passenger():
    # 최단거리 저장할 테이블
    dis_info = [[1e9 for _ in range(N)] for _ in range(N)]

    # 현재까지 최단거리 승객까지의 최단거리
    answer = 1e9
    min_passenger = -1
    min_passenger_x = N+1
    min_passenger_y = N+1

    cx, cy = CAR_POS
    q.append((cx, cy, 0))

    while q:
        x, y, dis = q.popleft()
        # print(x, y, dis)
        if MATRIX[x][y] != 'WALL' and MATRIX[x][y] > 0:
            # 승객 발견
            if dis < answer or (dis == answer and min_passenger_x > x) or (dis == answer and min_passenger_x == x and min_passenger_y > y):
                answer = dis
                min_passenger = MATRIX[x][y]
                min_passenger_x = x
                min_passenger_y = y

        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if in_range(nx, ny) and MATRIX[nx][ny] != 'WALL':
                if dis_info[nx][ny] > dis+1:
                    dis_info[nx][ny] = dis+1
                    q.append((nx, ny, dis+1))

    return min_passenger, min_passenger_x, min_passenger_y, answer


# 승객을 목적지로 데려다 주기 - bfs 돌려서 최단거리 구해내기
q2 = deque()

def ride(pid):
    global MATRIX

    # 최단거리 저장할 테이블
    dis_info = [[1e9 for _ in range(N)] for _ in range(N)]

    # 승객 목적지까지의 최단거리
    answer = 1e9

    cx, cy = CAR_POS
    q2.append((cx, cy, 0))

    while q2:
        x, y, dis = q2.popleft()
        if (x, y) == PASSENGER_DEST[pid]:
            # 목적지 발견
            if dis < answer:
                answer = dis

        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if in_range(nx, ny) and MATRIX[nx][ny] != 'WALL':
                if dis_info[nx][ny] > dis+1:
                    dis_info[nx][ny] = dis+1
                    q2.append((nx, ny, dis+1))

    return answer  


while True:
    # 1. 승객 고르기
    pid, x, y, dis = get_min_passenger()
    # print('선택된 승객, 거리', pid, dis)
    if pid == -1: # 이동 가능한 승객 없음
        break
    BATTERY -= dis
    # print('승객까지 이동 후 배터리', BATTERY)
    if BATTERY <= 0:
        break
    MATRIX[x][y] = 0
    CAR_POS = (x, y)
    # 2. 목적지로 데려다주기
    # PASSENGER_DEST[pid] 로 데려다 줘야 함
    move_dis = ride(pid)
    # print('목적지까지 거리', move_dis)
    BATTERY -= move_dis
    if BATTERY < 0:
        break
    BATTERY += move_dis*2
    FINISHED[pid] = 1
    CAR_POS = PASSENGER_DEST[pid]
    # print('승객 데려다준 후 배터리', BATTERY)
    # print('턴 종료 후 맵')
    # for _ in MATRIX:
    #     print(_)
if BATTERY < 0:
    BATTERY = -1
print(BATTERY)