R, C, K = map(int, input().split())

# 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


# 골룸의 현위치를 맵에 표시: 같은 번호(1~)는 같은 골룸이다.
# 골룸이 이동을 멈춘다면, 그때 이 맵을 갱신할 것
GOLLUM_STATE = [[0 for _ in range(C)] for _ in range(R)]


# 골룸들의 좌표. [(출구), (나머지1), (나머지1), (나머지1), (정가운데)]
# 맨 앞이 출구, 마지막이 중앙임을 유의할 것
# 초기 Gollum 중앙 행은 -2여야 함. 골렘의 최상단 좌표 행이 0까지 내려와야 진입 가능인 것
GOLLUMS_POS = []

# 출발하는 열 c, 골렘의 출구 방향 정보 d
for _ in range(K):
    c, d = map(int, input().split())
    gollums =[]
    mid_x, mid_y = -2, c-1
    for i in range(d, d+4):
        gollums.append([mid_x + dx[i%4], mid_y + dy[i%4]])
    gollums.append([mid_x, mid_y])
    GOLLUMS_POS.append(gollums)


def before_start(x, y):
    return x < 0

def in_range(x, y):
    return -1 < x < R and -1 < y < C


# 맵에 진입 가능?
# def can_join_game(gollum_pos):
#     can_join = True
#     for x, y in gollum_pos:
#         if before_start(x+3, y) or GOLLUM_STATE[x+3][y] != 0:
#             can_join = False
#             break
#     return can_join


def can_move_south(mid_pos):
    mid_x, mid_y = mid_pos[0], mid_pos[1]
    return (before_start(mid_x+1, mid_y-1) or (in_range(mid_x+1, mid_y-1) and GOLLUM_STATE[mid_x+1][mid_y-1] == 0)) \
            and (before_start(mid_x+2, mid_y) or (in_range(mid_x+2, mid_y) and GOLLUM_STATE[mid_x+2][mid_y] == 0)) \
            and (before_start(mid_x+1, mid_y+1) or (in_range(mid_x+1, mid_y+1) and GOLLUM_STATE[mid_x+1][mid_y+1] == 0))

def can_move_west(mid_pos):
    mid_x, mid_y = mid_pos[0], mid_pos[1]
    return (before_start(mid_x-1, mid_y-1) or (in_range(mid_x-1, mid_y-1) and GOLLUM_STATE[mid_x-1][mid_y-1] == 0)) \
            and (before_start(mid_x, mid_y-2) or (in_range(mid_x, mid_y-2) and GOLLUM_STATE[mid_x][mid_y-2] == 0)) \
            and (before_start(mid_x+1, mid_y-1) or (in_range(mid_x+1, mid_y-1) and GOLLUM_STATE[mid_x+1][mid_y-1] == 0)) \
            and (before_start(mid_x+1, mid_y-2) or (in_range(mid_x+1, mid_y-2) and GOLLUM_STATE[mid_x+1][mid_y-2] == 0)) \
            and (before_start(mid_x+2, mid_y-1) or (in_range(mid_x+2, mid_y-1) and GOLLUM_STATE[mid_x+2][mid_y-1] == 0)) 

def can_move_east(mid_pos):
    mid_x, mid_y = mid_pos[0], mid_pos[1]
    return (before_start(mid_x-1, mid_y+1) or (in_range(mid_x-1, mid_y+1) and GOLLUM_STATE[mid_x-1][mid_y+1] == 0)) \
            and (before_start(mid_x, mid_y+2) or (in_range(mid_x, mid_y+2) and GOLLUM_STATE[mid_x][mid_y+2] == 0)) \
            and (before_start(mid_x+1, mid_y+1) or (in_range(mid_x+1, mid_y+1) and GOLLUM_STATE[mid_x+1][mid_y+1] == 0)) \
            and (before_start(mid_x+1, mid_y+2) or (in_range(mid_x+1, mid_y+2) and GOLLUM_STATE[mid_x+1][mid_y+2] == 0)) \
            and (before_start(mid_x+2, mid_y+1) or (in_range(mid_x+2, mid_y+1) and GOLLUM_STATE[mid_x+2][mid_y+1] == 0))


# gid: 골룸 넘버. GOLLUM_STATE 의 번호(1이상)와 같다
# gollum의 5개 좌표를 받아서
# 이동 후 5개 좌표를 리턴 (0번째는 출구, 마지막은 중앙)
# 만약 이동 불가능할 경우 -1 리턴.
# 이 함수 호출한 곳에서 -1 받은 경우 최종위치 계산해야 함
#   단, 아직 맵에 진입 못한 경우면 카운트 하지 말고 GOLLUM_STATE 비우기
def move_gollum(gid, gollum_pos):  # GOLLUM_STATE 도 갱신해줘야?
    cant_go = False

    while True:
        # 남쪽
        if can_move_south(gollum_pos[-1]):
            # 골룸 상태 초기화
            for x, y in gollum_pos:
                if before_start(x, y):
                    pass
                else:
                    GOLLUM_STATE[x][y] = 0
            # 남쪽으로 이동 - 모든 칸의 행을 +1
            for i in range(5):
                gollum_pos[i][0] += 1
        else: # 출구 위치도 바꿔줄 것!!!!!!!!!!!!!!!!!!!!!!
            if can_move_west(gollum_pos[-1]): 
                # 골룸 상태 초기화
                for x, y in gollum_pos:
                    if before_start(x, y):
                        pass
                    else:
                        GOLLUM_STATE[x][y] = 0
                # 서쪽으로 이동 - 모든 칸의 열을 -1 한 다음
                for i in range(5):
                    gollum_pos[i][1] -= 1
                    gollum_pos[i][0] += 1
                # 출구 위치 갱신
                gollum_pos = [gollum_pos[3]] + gollum_pos[0:3] + [gollum_pos[4]]
                GOLLUMS_POS[gid-1] = gollum_pos
            elif can_move_east(gollum_pos[-1]):
                # 골룸 상태 초기화
                for x, y in gollum_pos:
                    if x < 0:
                        pass
                    else:
                        GOLLUM_STATE[x][y] = 0
                # 동쪽으로 이동 - 모든 칸의 열을 +1 한 다음
                for i in range(5):
                    gollum_pos[i][1] += 1
                    gollum_pos[i][0] += 1
                # 출구 위치 갱신
                gollum_pos = gollum_pos[1:4] + [gollum_pos[0]] + [gollum_pos[4]]
                GOLLUMS_POS[gid-1] = gollum_pos
            else:
                break
        
        for x, y in gollum_pos:
            if x >= 0:
                GOLLUM_STATE[x][y] = gid

    return gollum_pos

# MAX_ROW_OF[gid]은 gid 골룸에 속한 정령의 최대 행 값
MAX_ROW_OF = [0 for _ in range(K+1)] 


# 정령의 최종위치 구하기
def get_final_row(gid, gollum_pos):
    # 출구가 다른 골룸과 맞닿아 있다면 이동
    exit_x, exit_y = gollum_pos[0][0], gollum_pos[0][1]
    other_gollum_max_row = [] # 이동 가능한 다른 골룸 gid들의 MAX_ROW_OF 값

    for i in range(4):
        nx, ny = exit_x + dx[i], exit_y + dy[i]
        if in_range(nx, ny):
            if GOLLUM_STATE[nx][ny] != 0 and GOLLUM_STATE[nx][ny] != gid:
                other_gollum_max_row.append(MAX_ROW_OF[GOLLUM_STATE[nx][ny]])
    if len(other_gollum_max_row) != 0:
        MAX_ROW_OF[gid] = max(other_gollum_max_row)
    else: # 아니면 중앙에서 바로 아래 거 리턴
        MAX_ROW_OF[gid] = gollum_pos[-1][0] + 2


SUM_OF_MAX_ROW = 0

for k in range(K):
    res = move_gollum(k+1, GOLLUMS_POS[k])
    # move를 최대한으로 했는데도, 맵에 진입 못한 부분이 있다면 - STATE도 초기화
    cant_go = False
    for x, y in GOLLUMS_POS[k]:
        if before_start(x, y):
            cant_go = True
            break
    # move를 최대한으로 했는데도, 맵에 진입 못한 부분이 있다면 - STATE도 초기화
    if cant_go:
        # 게임 진입 불가
        # GOLLUM_STATE 초기화
        for x in range(R):
            for y in range(C):
                GOLLUM_STATE[x][y] = 0
        for i in range(1, K+1):
            MAX_ROW_OF[i] = 0
        continue
    get_final_row(k+1, GOLLUMS_POS[k])
    SUM_OF_MAX_ROW += MAX_ROW_OF[k+1]

print(SUM_OF_MAX_ROW)