N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

SCORE = 0

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N


# 기준점 찾기 - 그룹에 포함된 좌표들 전부 넣어주면 기준점 찾아줌
def find_point(group):
    point_x, point_y = -1, -1
    for x, y in group:
        if MATRIX[x][y] == 0: # red
            continue
        if x > point_x or (x == point_x and y < point_y):
            point_x, point_y = x, y
    return point_x, point_y


from collections import deque

q = deque()

def find_group(x, y):
    global visited

    bid = MATRIX[x][y]
    b_member = 1
    red_member = 0
    group = [(x, y)]

    q.append((x, y))
    visited[x][y] = True
    
    while q:
        r, c = q.popleft()
        for i in range(4):
            nr, nc = r+dx[i], c+dy[i]
            if in_range(nr, nc) and MATRIX[nr][nc] != 'e' and MATRIX[nr][nc] != -1 and not visited[nr][nc]:
                if MATRIX[nr][nc] == bid: # same color
                    b_member += 1
                    visited[nr][nc] = True
                elif MATRIX[nr][nc] == 0: # red
                    red_member += 1
                else:
                    continue
                q.append((nr, nc))
                group.append((nr, nc))

    return bid, b_member, red_member, find_point(group), group


def gravity_work():
    global MATRIX

    for col in range(N):
        for row in range(N-2, -1, -1):
            if MATRIX[row][col] == -1 or MATRIX[row+1][col] == -1:
                continue
            empty_cnt = 0
            for i in range(1, N-row):
                if MATRIX[row+i][col] == 'e':
                    empty_cnt += 1
                else:
                    break
            if empty_cnt > 0:
                MATRIX[row+empty_cnt][col] = MATRIX[row][col]
                MATRIX[row][col] = 'e'


# 반시계 90도 회전
def rotate():
    global MATRIX, new_matrix

    for t in range((N+1)//2):
        # 위 <- 오
        for i in range(t, N-t):
            new_matrix[t][i] = MATRIX[i][N-1-t]
        # 오 <- 아래
        for i in range(t, N-t):
            new_matrix[i][N-1-t] = MATRIX[N-1-t][N-1-i]
        # 아래 <- 왼
        for i in range(N-t-1, t-1, -1):
            new_matrix[N-1-t][i] = MATRIX[i][t]
        # 왼 <- 위
        for i in range(t, N-t):
            new_matrix[i][t] = MATRIX[t][N-1-i]

    for i in range(N):
        for j in range(N):
            MATRIX[i][j] = new_matrix[i][j]


while True:
    ''' === 1. 폭탄 그룹 찾기 === '''
    visited = [[False for _ in range(N)] for _ in range(N)]
    GROUP_INFO = []
    for i in range(N):
        for j in range(N):
            # 방문 전이고 돌이 아니고 빨간색도 아니고 빈곳도 아니면
            if not visited[i][j] and MATRIX[i][j] != 'e' and MATRIX[i][j] > 0:
                bid, b_member, red_member, point_pos, group = find_group(i, j)
                GROUP_INFO.append((bid, b_member, red_member, point_pos, group))
    # 만약 여기서 그룹이 없다면 break
    GAME_OVER = True
    for bid, b_member, red_member, point_pos, group in GROUP_INFO:
        if b_member+red_member > 1:
            GAME_OVER = False
            break
    if GAME_OVER:
        break

    ''' === 2. 폭탄 제거 === '''
    # 폭탄 선택
    max_member = 0
    max_bid, max_b_member, max_red_member, max_point_pos, max_group = -1, 0, 0, (-1, -1), []
    for bid, b_member, red_member, point_pos, group in GROUP_INFO:
        if b_member+red_member > max_member or\
        (b_member+red_member == max_member and max_red_member > red_member) or\
        (b_member+red_member == max_member and max_red_member == red_member and max_point_pos[0] < point_pos[0]) or\
        (b_member+red_member == max_member and max_red_member == red_member and max_point_pos[0] == point_pos[0] and max_point_pos[1] > point_pos[1]):
            max_bid, max_b_member, max_red_member, max_point_pos, max_group =\
                bid, b_member, red_member, point_pos, group
    # 폭탄 제거
    for x, y in max_group:
        MATRIX[x][y] = 'e' # empty
    SCORE += (max_b_member+max_red_member)**2
    # print('제거 후 M')
    # for _ in MATRIX:
    #     print(_)
    # 중력 작용
    gravity_work()
    # print('중력 후 M')
    # for _ in MATRIX:
    #     print(_)
    new_matrix = [[0 for _ in range(N)] for _ in range(N)]
    rotate()
    # print('회전 후 M')
    # for _ in MATRIX:
    #     print(_)
    # 중력 작용
    gravity_work()
    # print('중력 후 M')
    # for _ in MATRIX:
    #     print(_)
    # print(SCORE)
print(SCORE)