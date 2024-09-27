from collections import deque

N, L, R = map(int, input().split())
EGGS = [list(map(int, input().split())) for _ in range(N)]
TMP_EGGS = [[0 for _ in range(N)] for _ in range(N)]

# 아래, 우
dx = [-1, 0]
dy = [0, 1]
def in_range(x, y):
    return -1 < x < N and -1 < y < N

# 그룹으로 묶일 계란들 탐색
# start = [x, y]
def bfs(start):

    q = deque([start])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[start[0]][start[1]] = True
    group = [start]
    eggs_sum = EGGS[start[0]][start[1]]

    while q:
        x, y = q.popleft()
        for i in range(2):
            nx = x + dx[i]
            ny = y + dy[i]
            if in_range(nx, ny) and not visited[nx][ny] and L <= abs(EGGS[x][y] - EGGS[nx][ny]) <= R:
                q.append([nx, ny])
                visited[nx][ny] = True
                group.append([nx, ny])
                eggs_sum += EGGS[nx][ny]

    l = len(group)
    for r, c in group:
        TMP_EGGS[r][c] = eggs_sum // l

    return True if l > 1 else False


# VISITED = [[0 for _ in range(N)] for _ in range(N)]
for sec in range(1999):
    available = False
    # 합쳐질 계란들 집합 구하기
    for i in range(N):
        for j in range(N):
            if not TMP_EGGS[i][j]:
                res = bfs([i, j])
                if res == True:
                    available = True

    if not available:
        break       

    for i in range(N):
        for j in range(N):
            EGGS[i][j] = TMP_EGGS[i][j]
            TMP_EGGS[i][j] = 0

    # for _ in EGGS:
    #     print(_)
    # print()

print(sec)