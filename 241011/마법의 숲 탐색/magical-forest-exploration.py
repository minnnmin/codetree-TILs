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
            # print('남', end=' ')
            GOLLUM[gid] = (x+1, y, d)
        elif can_move_west(gid):
            # print('서', end=' ')
            GOLLUM[gid] = (x, y-1, (d+3)%4)
        elif can_move_east(gid):
            # print('동', end=' ')
            GOLLUM[gid] = (x, y+1, (d+1)%4)
        else:
            # print('이동 끝')
            break


# i번 골룸의 최대 행. 유니온 파인드st - 0번째 안씀
MAX_ROW = [0 for _ in range(K+1)]
# i번 골룸이랑 이어진 애. 본인 최대행보다 커야만 부모가 된다. 유니온 파인드st - 0번째 안씀
PARENTS = [i for i in range(K+1)]

# 정령번호 = 골룸번호 = gid로 치자 일단
for gid in range(1, K+1):
    # print('========= gid:', gid, '=========')
    ''' 1. 골룸 이동 '''
    move(gid)
 
    # 만약 골룸이 이동 했는데도 중심 행이 4 미만이면 그것도 맵 터짐
    x, y, d = GOLLUM[gid]
    if x < 4:
        # print('못 들어감')
        GOLLUM_MATRIX = [[0 for _ in range(C)] for _ in range(R)]
        continue
    else:
        GOLLUM_MATRIX[x][y] = gid
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            GOLLUM_MATRIX[nx][ny] = gid

    ''' 2. 정령 이동 후 전역변수 갱신 '''
    # gid번 정령의 이동
    x, y, d = GOLLUM[gid]
    MAX_ROW[gid] = x+1 # 본인 골룸 내 최대 행
    exit_x, exit_y = x+dx[d], y+dy[d]
    for i in range(4):
        nx, ny = exit_x+dx[i], exit_y+dy[i]
        if in_range(nx, ny) and GOLLUM_MATRIX[nx][ny] != gid: # 다른 골룸과 연결
            new_gid = GOLLUM_MATRIX[nx][ny]
            if MAX_ROW[PARENTS[gid]] < MAX_ROW[PARENTS[new_gid]]:
                PARENTS[gid] = PARENTS[new_gid]

    # exit_x, exit_y 상하좌우에 나랑 다른 번호 골룸 있으면 그 골룸이 내 부모가 됨
    # 저기모야. 맵 초과되어서 삭제될때 유니온 파인드도 초기화할것! - 이건 하지마. 마지막에 구해야 하니까.
    # 골룸 스테이트만 초기화.
    # print('부모 골룸', PARENTS)
    # print('최대 행', MAX_ROW)
    # print('골룸 매트릭스')
    # for _ in GOLLUM_MATRIX:
    #     print(_)
    # print('골룸 위치')
    # print(GOLLUM[gid])
    # if gid == 2:
    #     break


# 최종 출력 전, MAX_ROW를 3씩 뺄 것
for i in range(1, K+1):
    if MAX_ROW[i] != 0:
        MAX_ROW[i] -= 2
ANSWER = 0
# print(PARENTS)
# print(MAX_ROW)
for gid in range(1, K+1):
    ANSWER += MAX_ROW[PARENTS[gid]]
print(ANSWER)