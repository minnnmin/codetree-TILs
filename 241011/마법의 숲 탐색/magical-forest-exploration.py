R, C, K = map(int, input().split())
R += 3

# 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 맵에 사용할 행렬. 행: R+3, 열: C - 근데 이거 필요한가?
MATRIX = [[0 for _ in range(C)] for _ in range(R)]

# 현재 골룸들 상태. 골룸 번호(1~)가 적혀있다. 최종 이동 후 갱신할 것!
GOLLUM_MATRIX = [[0 for _ in range(C)] for _ in range(R)]

# 골룸 정보 (x, y, d): 중심의 위치와 출구 방향 - 0번 안씀
GOLLUM = [(-1, -1)]

for i in range(1, K+1):
    c, d = map(int, input().split())
    GOLLUM.append((1, c-1, d)) # 최초에 1행에서 출발

def in_range(x, y):
    return -1 < x < R and -1 < y < C

def can_move_south(gid):
    x, y, d = GOLLUM[gid]
    x1, y1 = x+1, y-1
    x2, y2 = x+2, y
    x3, y3 = x+1, y+1

    # 하나라도 범위 초과시 안 감
    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3)):
        return False
    # 하나라도 골룸이랑 겹치면 안 감
    if GOLLUM_MATRIX[x1][y1] + GOLLUM_MATRIX[x2][y2] + GOLLUM_MATRIX[x3][y3] != 0:
        return False
    return True

def can_move_west(gid):
    x, y, d = GOLLUM[gid]
    x1, y1 = x-1, y-1
    x2, y2 = x, y-2
    x3, y3 = x+1, y-1
    x4, y4 = x+1, y-2
    x5, y5 = x+2, y-1

    # 하나라도 범위 초과시 안 감
    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3) and in_range(x4, y4) and in_range(x5, y5)):
        return False
    # 하나라도 골룸이랑 겹치면 안 감
    if GOLLUM_MATRIX[x1][y1] + GOLLUM_MATRIX[x2][y2] + GOLLUM_MATRIX[x3][y3] + GOLLUM_MATRIX[x4][y4] + GOLLUM_MATRIX[x5][y5] != 0:
        return False

    return True

def can_move_east(gid):
    x, y, d = GOLLUM[gid]
    x1, y1 = x-1, y+1
    x2, y2 = x, y+2
    x3, y3 = x+1, y+1
    x4, y4 = x+2, y+1
    x5, y5 = x+1, y+2

    # 하나라도 범위 초과시 안 감
    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3) and in_range(x4, y4) and in_range(x5, y5)):
        return False
    # 하나라도 골룸이랑 겹치면 안 감
    if GOLLUM_MATRIX[x1][y1] + GOLLUM_MATRIX[x2][y2] + GOLLUM_MATRIX[x3][y3] + GOLLUM_MATRIX[x4][y4] + GOLLUM_MATRIX[x5][y5] != 0:
        return False

    return True


# gid 최대한 이동시키기
def move(gid):
    global GOLLUM
    while 1:
        x, y, d = GOLLUM[gid]
        if can_move_south(gid):
            GOLLUM[gid] = (x+1, y, d)
        elif can_move_west(gid):
            GOLLUM[gid] = (x, y-1, (d+3)%4)
        elif can_move_east(gid):
            GOLLUM[gid] = (x, y+1, (d+1)%4)
        else:
            break

# 최대 행 합
ANSWER = 0

from collections import deque

q = deque()

# 정령 이동 - bfs
def move2(gid):
    global GOLLUM_MATRIX, ANSWER, MAX_ROW
    x, y, d = GOLLUM[gid]
    MAX_ROW[gid] = x+1-2
    tx, ty = x+dx[d], y+dy[d] # 출구를 넣고 돌려
    visited = [[False for _ in range(C)] for _ in range(R)]
    visited[tx][ty] = True
    q.append((tx, ty, gid))


    while q:
        x, y, g = q.popleft()
        MAX_ROW[gid] = MAX_ROW[g] if MAX_ROW[g] > MAX_ROW[gid] else MAX_ROW[gid]

        tx, ty, td = GOLLUM[g]
        if (x, y) == (tx+dx[td], ty+dy[td]):
            # 출구 이므로! 다른 애들 추가 가능
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny) and GOLLUM_MATRIX[nx][ny] > 0 and not visited[nx][ny]:
                    q.append((nx, ny, GOLLUM_MATRIX[nx][ny]))
                    visited[nx][ny] = True
    ANSWER += MAX_ROW[gid]


# i번 골룸의 최대 행. 유니온 파인드st - 0번째 안씀
MAX_ROW = [0 for _ in range(K+1)]
# i번 골룸이랑 이어진 애. 본인 최대행보다 커야만 부모가 된다. 유니온 파인드st - 0번째 안씀
PARENTS = [i for i in range(K+1)]


# 정령번호 = 골룸번호 = gid로 치자 일단
for gid in range(1, K+1):
    ''' 1. 골룸 이동 '''
    move(gid)
 
    # 만약 골룸이 이동 했는데도 중심 행이 4 미만이면 그것도 맵 터짐
    x, y, d = GOLLUM[gid]
    if x < 4:
        GOLLUM_MATRIX = [[0 for _ in range(C)] for _ in range(R)]
        continue
    else:
        GOLLUM_MATRIX[x][y] = gid
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            GOLLUM_MATRIX[nx][ny] = gid

    ''' 2. 정령 이동 후 전역변수 갱신 '''
    move2(gid)
 
print(ANSWER)