N, M = map(int, input().split())
BASECAMP = [list(map(int, input().split())) for _ in range(N)]

# i번 사람의 편의점 위치
STORE = [None]
# i번 사람의 현재 위치 - 베이스 캠프 들어오면서 위치 추가됨
# 만약 편의점 도착 시, 'finish'로 바꿀 것
PEOPLE_POS = [None]
# 편의점 도착한 사람 수
FINISH_N = 0

for _ in range(M):
    x, y = map(int, input().split())
    STORE.append([x-1, y-1])

# 베이스캠프 입성, 편의점 도착 시 1로 갱신
CANT_GO = [[0 for _ in range(N)] for _ in range(N)]


# 상좌우하
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

from collections import deque

q = deque()
def find_basecamp(num):
    # 해당 사람의 편의점 위치에서 BFS를 돌리면서 가장 가까우면서 행 작고 열 작은 베캠 찾기
    visited = [[False for _ in range(N)] for _ in range(N)]

    store_x, store_y = STORE[num]
    visited[store_x][store_y] = True
    q.append((store_x, store_y, 0))

    min_dis, min_x, min_y = 300, 30, 30
    
    while q:
        x, y, dis = q.popleft()
        if not CANT_GO[x][y] and BASECAMP[x][y]:
            if dis < min_dis or (dis == min_dis and min_x > x) or (dis == min_dis and min_x == x and min_y > y):
                min_dis, min_x, min_y = dis, x, y
        else:
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny) and not visited[nx][ny] and not CANT_GO[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny, dis+1))
    
    return min_x, min_y


q2 = deque()
def move(num):
    global PEOPLE_POS
    # num번 사람을 상하좌우로 이동시켜 자신의 편의점에 가까워지도록 (최단거리여야 함)
    # 최단거리 중복 시, 상-좌-우-하 우선 순
    visited = [[False for _ in range(N)] for _ in range(N)]
    px, py = PEOPLE_POS[num]
    visited[px][py] = True
    q2.append((px, py, 0, []))
    min_dis = 300
    dir_history = [4] # 이동한 방향 저장 - 대소 비교를 위해 4 넣어둠. 방향: 0~3이니까.

    while q2:
        x, y, dis, history = q2.popleft()
        if [x, y] == STORE[num]:
            if dis < min_dis or (dis == min_dis and history < dir_history):
                min_dis, dir_history = dis, history
        else:
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny) and not CANT_GO[nx][ny] and not visited[nx][ny]:
                    q2.append((nx, ny, dis+1, history + [i]))
                    visited[nx][ny] = True
    nd = dir_history[0]
    px, py = px+dx[nd], py+dy[nd]
    PEOPLE_POS[num] = [px, py]
    


minutes = 1
while 1:
    if FINISH_N == M:
        break
    ''' 1. 격자 내 모든 사람 1칸 이동 '''
    now_people_cnt = len(PEOPLE_POS) - 1
    for num in range(1, now_people_cnt+1):
        if PEOPLE_POS[num] != 'finish':
            move(num)

    ''' 2. 새로 편의점 도착한 사람 있는지 확인 '''
    for num in range(1, now_people_cnt+1):
        # print(num, '번 도착했는지 확인')
        if PEOPLE_POS[num] == 'finish':
            continue
        if PEOPLE_POS[num] == STORE[num]:
            sx, sy = STORE[num]
            CANT_GO[sx][sy] = 1
            PEOPLE_POS[num] = 'finish'
            FINISH_N += 1
    # print('도착한 사람')
    # print(PEOPLE_POS)

    ''' 3. 사람 추가 '''
    if minutes <= M:
        base_x, base_y = find_basecamp(minutes)
        # print(minutes, '번 추가')
        PEOPLE_POS.append([base_x, base_y])
        # print(PEOPLE_POS)
        CANT_GO[base_x][base_y] = 1
    minutes += 1
    # if minutes == 5:
    #     print('끝')
    #     break
print(minutes-1)