R, C, K = map(int, input().split())
R += 3

# 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

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

    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3)):
        return False
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

    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3) and in_range(x4, y4) and in_range(x5, y5)):
        return False
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

    if not (in_range(x1, y1) and in_range(x2, y2) and in_range(x3, y3) and in_range(x4, y4) and in_range(x5, y5)):
        return False
    if GOLLUM_MATRIX[x1][y1] + GOLLUM_MATRIX[x2][y2] + GOLLUM_MATRIX[x3][y3] + GOLLUM_MATRIX[x4][y4] + GOLLUM_MATRIX[x5][y5] != 0:
        return False

    return True


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


def move2(gid):
    global GOLLUM_MATRIX, ANSWER, MAX_ROW
    x, y, d = GOLLUM[gid]
    MAX_ROW[gid] = x+1-2
    tx, ty = x+dx[d], y+dy[d]
    visited = [[False for _ in range(C)] for _ in range(R)]
    visited[tx][ty] = True
    q.append((tx, ty, gid))


    while q:
        x, y, g = q.popleft()
        MAX_ROW[gid] = MAX_ROW[g] if MAX_ROW[g] > MAX_ROW[gid] else MAX_ROW[gid]

        tx, ty, td = GOLLUM[g]
        if (x, y) == (tx+dx[td], ty+dy[td]):
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny) and GOLLUM_MATRIX[nx][ny] > 0 and not visited[nx][ny]:
                    q.append((nx, ny, GOLLUM_MATRIX[nx][ny]))
                    visited[nx][ny] = True
    
    ANSWER += MAX_ROW[gid]
    print(ANSWER, end=' ')


MAX_ROW = [0 for _ in range(K+1)]
PARENTS = [i for i in range(K+1)]


for gid in range(1, K+1):
    ''' 1. 골룸 이동 '''
    move(gid)
 
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