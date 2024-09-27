from collections import deque

N, L, R = map(int, input().split())
EGGS = [list(map(int, input().split())) for _ in range(N)]
TMP_EGGS = [[0 for _ in range(N)] for _ in range(N)]

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
def in_range(x, y):
    return -1 < x < N and -1 < y < N

# 그룹으로 묶일 계란들 탐색
# start = (x, y)

q = deque()
visited = [[False for _ in range(N)] for _ in range(N)]

def bfs():
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if in_range(nx, ny) and not visited[nx][ny] and L <= abs(EGGS[x][y] - EGGS[nx][ny]) <= R:
                q.append((nx, ny))
                visited[nx][ny] = True
                group.append((nx, ny))


for sec in range(1999):
    # 합쳐질 계란들 집합 구하기
    
    for i in range(N):
        for j in range(N):
            visited[i][j] = False

    is_changed = False

    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                group = []
                
                q.append((i, j))
                group.append((i, j))
                visited[i][j] = True

                bfs()

                if len(group) > 1:
                    is_changed = True

                sum_of_eggs = 0
                for x, y in group:
                    sum_of_eggs += EGGS[x][y]
                
                for x, y in group:
                    EGGS[x][y] = sum_of_eggs // len(group)

    # for _ in EGGS:
    #     print(_)
    # print()
    if not is_changed:
        break

print(sec)