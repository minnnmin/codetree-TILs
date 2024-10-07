N, M, K = map(int, input().split())
# MONO_TURN = {K: []} # MONO_TURN[i] = [(1, 2), (3, 4)] i턴에 두 좌표 독점 풀림
DEAD = [0 for _ in range(M+1)] # 0 안씀
PLAYER_POS_D = {} # 플레이어들 현위치와 방향. pid: (x, y, d)

# 독점 정보
MONOPOLY = [[0 for _ in range(N)] for _ in range(N)]

# 말들의 현위치
MATRIX = [list(map(int, input().split())) for _ in range(N)]
tmp_dir = list(map(int, input().split()))

for i in range(N):
    for j in range(N):
        if MATRIX[i][j] > 0:
            pid = MATRIX[i][j]
            PLAYER_POS_D[pid] = (i, j, tmp_dir[pid-1]-1)
            MONOPOLY[i][j] = [pid, K]

PRIORITY = [[] for _ in range(M+1)] # 각 플레이어 이동 우선순위. 0번째 안씀
for pid in range(1, M+1):
    for i in range(4):
        a, b, c, d = list(map(int, input().split()))
        PRIORITY[pid].append((a-1, b-1, c-1, d-1))

# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

from copy import deepcopy

for turn in range(1001):
    # 독점계약 해지되는 애들 풀어주기
    if DEAD.count(0) == 2:
        break
    for i in range(N):
        for j in range(N):
            if MONOPOLY[i][j] == 0:
                continue
            elif MONOPOLY[i][j][1] == 0:
                MONOPOLY[i][j] = 0

    new_matrix = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if MONOPOLY[i][j] != 0:
                MONOPOLY[i][j][1] -= 1

    # 플레이어 이동
    for pid in range(1, M+1):
        x, y, d = PLAYER_POS_D[pid]
        nx, ny, nd = x, y, d
        if DEAD[pid]:
            continue
        # 독점계약 없는 칸으로 이동 가능한지 확인
        can_get_monopoly = False
        
        for next_dir in PRIORITY[pid][d]:
            next_x, next_y = x+dx[next_dir], y+dy[next_dir]
            if in_range(next_x, next_y) and MONOPOLY[next_x][next_y] == 0:
                nx, ny, nd = next_x, next_y, next_dir
                can_get_monopoly = True
                if new_matrix[nx][ny] > 0:
                    # 죽는 거야..
                    DEAD[pid] = 1
                    break
                new_matrix[nx][ny] = pid
                PLAYER_POS_D[pid] = (nx, ny, nd)
                break
        # 독점 불가. 그럼 내 위치로 이동
        if not can_get_monopoly:
            for next_dir in PRIORITY[pid][d]:
                next_x, next_y = x+dx[next_dir], y+dy[next_dir]
                if in_range(next_x, next_y) and MONOPOLY[next_x][next_y][0] == pid:
                    nx, ny, nd = next_x, next_y, next_dir
                    new_matrix[nx][ny] = pid
                    PLAYER_POS_D[pid] = (nx, ny, nd)
                    break
    # 자 이제 new_matrix에 있는 애들은 해당 위치를 독점시켜
    # MONO_TURN[turn+K] = []
    for i in range(N):
        for j in range(N):
            pid = new_matrix[i][j]
            if pid > 0:
                MONOPOLY[i][j] = [pid, K]
            MATRIX[i][j] = pid
if turn >= 1000:
    turn = -1
print(turn)

# print('이동 후')
# for _ in MATRIX:
#     print(_)
# print(PLAYER_POS_D)
# for _ in MONOPOLY:
#     print(_)