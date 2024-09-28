N, K = map(int, input().split())

# 윷판 색깔
GAME_MAP = [list(map(int, input().split())) for _ in range(N)]

# PLAYER 길이는 K+1
PLAYER = [[]] # PLAYER[i]는 i번 말의 위치와 방향. 0번째 말은 없으므로 그냥 비워둠
for _ in range(K):
    x, y, d = map(int, input().split())
    PLAYER.append([x-1, y-1, d-1])

# 윷놀이 판 현황 (말들 쌓여있는 정보 알 수 있음)
PLAYING_GAME = [[[] for _ in range(N)] for _ in range(N)]
for player_num in range(1, len(PLAYER)):
    x, y, f = PLAYER[player_num]
    PLAYING_GAME[x][y].append(player_num)

# 오, 왼, 상, 하
dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]

# print('게임 전')
# for _ in PLAYER:
#     print(_)
# print()

# for _ in PLAYING_GAME:
#     print(_)


def in_range(x, y):
    return -1 < x < N and -1 < y < N


def change_dir(d):
    if d == 0:
        return 1
    elif d == 1:
        return 0
    elif d == 2:
        return 3
    elif d == 3:
        return 2


# x, y는 이동 전 위치, nx, ny는 이동하려는 위치, blue에서 호출한 경우 d로 방향 바꿔줘야 함, 나머지는 기존 방향 그대로 넣기
# height는 말의 높이 - 이 이상으로만 같이 이동해야 함
def white(x, y, nx, ny, d, height, player_num):
    
    PLAYER[player_num][2] = d

    # 새 위치 갱신(추가)
    PLAYING_GAME[nx][ny] += PLAYING_GAME[x][y][height:]

    # 잠만 PLAYER들의 위치값도 갱신해 줘야 함
    for player_num in PLAYING_GAME[x][y][height:]:
        PLAYER[player_num][0] = nx
        PLAYER[player_num][1] = ny

    # 전 위치 갱신(삭제)
    PLAYING_GAME[x][y] = PLAYING_GAME[x][y][:height]


# 이동하려는 칸이 레드면?
# 현재 위치에 있던 애들의 순서를 뒤집은 후 다함께 이동
def red(x, y, nx, ny, d, height, player_num):
    
    PLAYER[player_num][2] = d

    # 새 위치 갱신(추가)
    new_list = reversed(PLAYING_GAME[x][y][height:])
    PLAYING_GAME[nx][ny] += new_list

    # 잠만 PLAYER들의 위치값도 갱신해 줘야 함
    for player_num in PLAYING_GAME[x][y][height:]:
        PLAYER[player_num][0] = nx
        PLAYER[player_num][1] = ny

    # 전 위치 갱신(삭제)
    PLAYING_GAME[x][y] = PLAYING_GAME[x][y][:height]


# 이동하려는 칸이 파란색이라면?
# '내 방향'만 뒤집어서 새로운 이동칸의 색을 확인
# 그 칸이 흰색, 빨간색이면 위 함수를 사용하고
# 그 칸이 블루면 이번에는 이동하지 않고 그냥 끝냄
# 새 위치 값을 갱신하고
# 전 위치 값을 clear
def blue(x, y, nx, ny, d, height, player_num):
    # 1. 내 방향만 반대로 바꿔서 또 확인
    nd = change_dir(d)

    nnx, nny = x+dx[nd], y+dy[nd]
    if in_range(nnx, nny):
        color = GAME_MAP[nnx][nny]
        if color == 0:
            white(x, y, nnx, nny, nd, height, player_num)
        elif color == 1:
            red(x, y, nnx, nny, nd, height, player_num)
        elif color == 2:
            PLAYER[player_num][2] = nd
    else:
        PLAYER[player_num][2] = nd


def not_available():
    for i in range(N):
        for j in range(N):
            if len(PLAYING_GAME[i][j]) >= 4:
                return True
    return False


t = 0
# # # 불가능한 경우가 있나?
while t < 77:
    t += 1
    # 말 하나씩 꺼내서 순서대로 이동
    MUST_STOP = False
    for player_num in range(1, K+1):
        x, y, d = PLAYER[player_num] # 이 말의 차례다
        nx, ny = x+dx[d], y+dy[d]
        if in_range(nx, ny):
            color = GAME_MAP[nx][ny]
            if color == 0: # white
                white(x, y, nx, ny, d, PLAYING_GAME[x][y].index(player_num), player_num)
            elif color == 1: # red
                red(x, y, nx, ny, d, PLAYING_GAME[x][y].index(player_num), player_num)
            elif color == 2: # blue
                blue(x, y, nx, ny, d, PLAYING_GAME[x][y].index(player_num), player_num)
        else:
            # 블루랑 똑같이 진행
            # print(x, y, PLAYING_GAME[x][y], player_num, t)
            blue(x, y, nx, ny, d, PLAYING_GAME[x][y].index(player_num), player_num)
        if not_available():
            MUST_STOP = True
            break
    if MUST_STOP:
        break
    
    # t += 1
    # 말 4개 이상이 겹쳐지면 break
    # not_available = False
    # for i in range(N):
    #     for j in range(N):
    #         if len(PLAYING_GAME[i][j]) >= 4:
    #             not_available = True

    # if not_available():
    #     break       
    

# print('게임 후')
# for _ in PLAYER:
#     print(_)
# print()

# for _ in PLAYING_GAME:
#     print(_)

print(t)