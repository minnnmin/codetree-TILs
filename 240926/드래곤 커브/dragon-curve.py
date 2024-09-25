X, Y = 100, 100
N = int(input())
dragon_curve = [list(map(int, input().split())) for _ in range(N)]
MATRIX = [[0 for _ in range(100)] for _ in range(100)]


# 방향 d: 0, 1, 2, 3이 각각 오, 위, 왼, 아
dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]


# 회전 시 이동해야 하는 방향(직전이 last_dir였으면 next_dir로 이동해야 함)
def next_dir(last_dir):
    if last_dir == 0:
        next_dir = 1
    elif last_dir == 1:
        next_dir = 2
    elif last_dir == 2:
        next_dir = 3
    elif last_dir == 3:
        next_dir = 0
    
    return next_dir


# 정사각형 세기
def count_square():
    res = 0
    for i in range(99):
        for j in range(99):
            if MATRIX[i][j] and MATRIX[i][j+1] and MATRIX[i+1][j] and MATRIX[i+1][j+1]:
                res += 1

    return res              


# (x, y)는 끝점, 방향, 차수
for x, y, d, g in dragon_curve:
    # 0차
    MATRIX[x][y] = 1
    x = x + dx[d]
    y = y + dy[d]
    MATRIX[x][y] = 1
    history = [d]
    for _ in range(g): # 1~g차
        tmp_history = []
        for his in history[::-1]:
            nd = next_dir(his)
            x += dx[nd]
            y += dy[nd]
            MATRIX[x][y] = 1
            tmp_history.append(nd)
        for th in tmp_history:
            history.append(th)

print(count_square())