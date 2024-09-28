N, M, K = map(int, input().split())
MOLD = [[[] for _ in range(M)] for _ in range(N)]
for _ in range(K):
    x, y, s, d, b = map(int, input().split())
    MOLD[x-1][y-1].append([s, d-1, b])

# for _ in MOLD:
#     print(_)

    
MOLD_SIZE_SUM = 0


# 0, 1, 2, 3
# 상, 하, 우, 좌
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]


def in_range(x, y):
    return -1 < x < N and -1 < y < M


def change_dir(d):
    if d == 0:
        return 1
    elif d == 1:
        return 0
    elif d == 2:
        return 3
    elif d == 3:
        return 2
        

# 해당 열 검사
def check_mold(col):
    global MOLD_SIZE_SUM

    for i in range(N):
        if MOLD[i][col] != []: # 곰팡이 있으면 채취
            print('먹는다', MOLD[i][col])
            MOLD_SIZE_SUM += MOLD[i][col][0][2]
            MOLD[i][col] = []
            return
    return


# 이동할 곰팡이 정보를 다른 곳에 저장해 두고,
# 모든 이동 검사가 끝나면 그때 갱신 (원래 거 지우고, 새로운 곳에 append)
MOVE_MOLD = [] # (nx, ny, s, d, b) nx, ny는 새 위치


# 곰팡이 이동 - 이 때는 겹쳐지는 애가 없다고 가정 (왜냐? 최초에 없고, 이후로는 매번 겹치는 애들을 처리할 거니까)
def move_mold():
    for x in range(N):
        for y in range(M):
            if MOLD[x][y] != []: # s, d, b 속력, 방향, 크기
                s, d, b = MOLD[x][y][0]
                nx, ny = x, y
                for tmp in range(s):
                    if not in_range(nx + dx[d], ny + dy[d]):
                        d = change_dir(d)
                        nx, ny = nx + dx[d], ny + dy[d]
                    else:
                        nx, ny = nx + dx[d], ny + dy[d]
                # if not -1 < nx < N:
                #     print('hi')
                MOVE_MOLD.append([nx, ny, s, d, b])
                MOLD[x][y] = []


# 한 곳에 곰팡이 2개 이상이면 처리
def del_mold():
    for x in range(N):
        for y in range(M):
            if len(MOLD[x][y]) > 1:
                # print(len(MOLD[x][y]))
                s, d, b = MOLD[x][y][0]
                for mold in MOLD[x][y][1:]:
                    if mold[2] > b:
                        s, d, b = mold[0], mold[1], mold[2]
                # print(s, d, b)
                MOLD[x][y] = [[s, d, b]]


for i in range(M):
    check_mold(i)
    move_mold()
    # print('MOVE_MOLD', MOVE_MOLD)
    for nx, ny, s, d, b in MOVE_MOLD:
        MOLD[nx][ny].append([s, d, b])
    MOVE_MOLD = []
    del_mold()
    # for i in range(4):
    #     print(MOLD[i])
    # print()

print(MOLD_SIZE_SUM)