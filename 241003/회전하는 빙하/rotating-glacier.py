from collections import deque

N, Q = map(int, input().split())
ICE = [list(map(int, input().split())) for _ in range(2**N)]
ORDER = list(map(int, input().split())) # 회전해야 하는 레벨이 순서대로 들어있음


# 구역 나눠진 다음, 회전해야 하는 각 사각형의 왼쪽 꼭지점과 레벨 L을 전달하면, 회전시킴
def rotate(X, Y, L):
    global ICE

    # 좌상 -> 우상
    for x in range(X, X+2**(L-1)):
        for y in range(Y, Y+2**(L-1)):
            NEW[x][y+2**(L-1)] = ICE[x][y]
    # 우상 -> 우하
    for x in range(X, X+2**(L-1)):
        for y in range(Y+2**(L-1), Y+2**L):
            NEW[x+2**(L-1)][y] = ICE[x][y]
    # 우하 -> 좌하
    for x in range(X+2**(L-1), X+2**L):
        for y in range(Y+2**(L-1), Y+2**L):
            NEW[x][y-2**(L-1)] = ICE[x][y]
    # 좌하 -> 좌상
    for x in range(X+2**(L-1), X+2**L):
        for y in range(Y, Y+2**(L-1)):
            NEW[x-2**(L-1)][y] = ICE[x][y]

    # for i in range(X, X+2**L):
    #     for j in range(Y, Y+2**L):
    #         ICE[i][j] = NEW[i][j]

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < 2**N and -1 < y < 2**N

# 빙하 녹이기
def melting_ice():
    global ICE, NEW

    for x in range(2**N):
        for y in range(2**N):
            cnt = 0
            if ICE[x][y] != 0:
                # 상하좌우 보고 1이상인 거 개수 세기
                for i in range(4):
                    nx, ny = x+dx[i], y+dy[i]
                    if in_range(nx, ny) and ICE[nx][ny] > 0:
                        cnt += 1
                if cnt < 3:
                    NEW[x][y] = ICE[x][y] - 1
                else:
                    NEW[x][y] = ICE[x][y]
    
    for i in range(2**N):
        for j in range(2**N):
            ICE[i][j] = NEW[i][j]


# 가장 큰 군집 구하기
ANSWER_MAX_GROUP_MEMBER = 0

q = deque()

def bfs(x, y, gid):
    global ANSWER_MAX_GROUP_MEMBER, GROUP, q, visited
    
    q.append((x, y))
    visited[x][y] = True
    GROUP[x][y] = gid
    member_cnt = 1

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if in_range(nx, ny) and ICE[nx][ny] > 0 and not visited[nx][ny]:
                member_cnt += 1
                visited[nx][ny] = True
                GROUP[nx][ny] = gid
                q.append((nx, ny))

    if member_cnt > ANSWER_MAX_GROUP_MEMBER:
        ANSWER_MAX_GROUP_MEMBER = member_cnt


for L in ORDER:
    # 레벨에 따라 회전 - 레벨 0일 수도 있다. 당연 회전은 안 일어나
    if L != 0:
        NEW = [[0 for _ in range(2**N)] for _ in range(2**N)]
        for x in range(0, 2**N, 2**L):
            for y in range(0, 2**N, 2**L):
                rotate(x, y, L)
        # ICE 갱신
        for i in range(2**N):
            for j in range(2**N):
                ICE[i][j] = NEW[i][j]
    # 얼음 녹이기
    NEW = [[0 for _ in range(2**N)] for _ in range(2**N)]
    melting_ice()

# 빙하의 총 양
ANSWER_ICE = 0
for i in range(2**N):
    for j in range(2**N):
        ANSWER_ICE += ICE[i][j] 
print(ANSWER_ICE)

# 군집 구하기
# gid 1씩 늘려가며 bfs 호출
GROUP = [[0 for _ in range(2**N)] for _ in range(2**N)]
gid = 1
for i in range(2**N):
    for j in range(2**N):
        if GROUP[i][j] == 0 and ICE[i][j] != 0:
            visited = [[False for _ in range(2**N)] for _ in range(2**N)]
            bfs(i, j, gid)
            gid += 1
print(ANSWER_MAX_GROUP_MEMBER)