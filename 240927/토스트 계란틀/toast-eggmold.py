from collections import deque

N, L, R = map(int, input().split())
EGGS = [list(map(int, input().split())) for _ in range(N)]


# 0이 아니라면 BFS가 지나간 곳임. 이 역시 매 초마다 초기화
# VISITED = [[0 for _ in range(N)] for _ in range(N)]


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def in_range(x, y):
    return -1 < x < N and -1 < y < N


# 그룹으로 묶일 계란들 탐색
# GROUP에 gid 표시
# start = [x, y]
def bfs(start, gid):

    VISITED[start[0]][start[1]] = gid

    q = deque([start])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[start[0]][start[1]] = True

    group = [start]
    eggs_sum = EGGS[start[0]][start[1]]


    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if in_range(nx, ny) and not visited[nx][ny] and L <= abs(EGGS[x][y] - EGGS[nx][ny]) <= R:
                q.append([nx, ny])
                VISITED[nx][ny] = gid
                visited[nx][ny] = True
                group.append([nx, ny])
                eggs_sum += EGGS[nx][ny]

    return group, eggs_sum

VISITED = [[0 for _ in range(N)] for _ in range(N)]
for sec in range(2000):
    group_and_eggsum = [] # [group에 속하는 애들 좌표리스트, 계란의 합]
    for x in range(N):
        for y in range(N):
            VISITED[x][y] = 0

    available = False
    # 합쳐질 계란들 집합 구하기
    for i in range(N):
        for j in range(N):
            if not VISITED[i][j]:
                group, eggs_sum = bfs([i, j], sec)
                if len(group) != 1:
                    group_and_eggsum.append([group, eggs_sum])
                    available = True
    # print(group, eggs_sum)
    if not available:
        break         

    # 계란 합치기 진행
    for g, es in group_and_eggsum:
        l = len(g)
        for x, y in g:
            EGGS[x][y] = es // l

    # for _ in EGGS:
    #     print(_)
    # print()


print(sec)