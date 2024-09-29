# 격자 크기 N, 리브로수를 키우는 총 년 수 M
N, M = map(int, input().split())

TREES = [list(map(int, input().split())) for _ in range(N)]
MOVE_ORDER = [list(map(int, input().split())) for _ in range(M)]

# 1이면 영양제 있는 거
# (d, p) 이동 방향 d, 이동 칸 수 p
# SUPPLEMENTS = [[0 for _ in range(N)] for _ in range(N)]
# SUPPLEMENTS[N-2][0], SUPPLEMENTS[N-2][1], SUPPLEMENTS[N-1][0], SUPPLEMENTS[N-1][1] = 1, 1, 1, 1
SUPPLEMENTS = [(N-2, 0), (N-2, 1), (N-1, 0), (N-1, 1)]

# for _ in SUPPLEMENTS:
#     print(_)

# 이동방향 1~8 (0번째 거 안씀)
dx = ['a', 0, -1, -1, -1, 0, 1, 1, 1]
dy = ['a', 1, 1, 0, -1, -1, -1, 0, 1]


def in_range(x, y):
    return -1 < x < N and -1 < y < N

def change_pos(x, y):
    if x >= N:
        x -= (x // N)*N
    elif x < 0:
        if -x % N == 0:
            x += (-x // N)*N
        else:
            x += (-x // N + 1)*N
    if y >= N:
        y -= (y // N)*N
    elif y < 0:
        if -y % N == 0:
            y += (-y // N)*N
        else:
            y += (-y // N + 1)*N
    return x, y


# 영양제 이동
# 이동 방향 d, 이동 칸 수 p
def move_supplments(d, p):
    global SUPPLEMENTS
    NEW_SUPPLEMENTS = []

    for x, y in SUPPLEMENTS:
        x, y = change_pos(x + dx[d]*p, y + dy[d]*p)
        NEW_SUPPLEMENTS.append((x, y))

    SUPPLEMENTS = NEW_SUPPLEMENTS


# (x, y)에 있는 나무의 인접 대각선을 확인해서(범위 내) 높이 1이상인 나무의 개수 리턴
def adj_tree_cnt(x, y):
    res = 0
    for i in range(2, 9, 2): # 인접대각선은 2, 4, 6, 8
        nx, ny = x + dx[i], y + dy[i]
        if in_range(nx, ny) and TREES[nx][ny] > 0:
            res += 1
    return res


# 나무 성장
def grow_trees():
    global TREES, SUPPLEMENTS

    # 영양제를 맞은 나무 정보가 따로 있어야 함.
    # 그래야 나머지만 가지고 -2 처리 해줌
    for x, y in SUPPLEMENTS:
        TREES[x][y] += 1

    # 영양제 맞은 나무 인접 대각선 확인해서, 높이가 1이상인 개수만큼 높이 ++
    for x, y in SUPPLEMENTS:
        TREES[x][y] += adj_tree_cnt(x, y)
    
    # 영양제 안 맞은 애들 높이 -2 깎고 거기에 영양제 뿌려
    NEW_SUPPLEMENTS = []
    # 기존 영양제 위치 리셋
    for x in range(N):
        for y in range(N):
            if (x, y) not in SUPPLEMENTS and TREES[x][y] >= 2:
                TREES[x][y] -= 2
                NEW_SUPPLEMENTS.append((x, y))
    
    SUPPLEMENTS = NEW_SUPPLEMENTS


# 이동 방향 d, 이동 칸 수 p
for d, p in MOVE_ORDER:
    move_supplments(d, p) # 이거 끝나면 SUPPLEMENTS 갱신
    grow_trees() # 이거 끝나면 TREES, SUPPLEMENTS 갱신

TREE_HEIGHT_SUM = 0
for i in range(N):
    for j in range(N):
        TREE_HEIGHT_SUM += TREES[i][j]

print(TREE_HEIGHT_SUM)