# 크기, 턴, 산타수, 루돌프 힘, 산타 힘
N, M, P, C, D = map(int, input().split())
RX, RY = map(int, input().split())
RX, RY = RX-1, RY-1

# 기절 여부. 각 칸에는 깨어날 턴이 적혀있다. - 0번째는 안씀
PASS_OUT = [False for _ in range(P+1)]
# 탈락 여부. True면 탈락임 - 0번째는 안씀
GAME_OVER = [False for _ in range(P+1)]
# 산타 점수 - 0번째는 안씀
SCORE = [0 for _ in range(P+1)] 
# 산타 위치 - 0번째는 안씀
SANTA_POS = [0 for _ in range(P+1)]
# 이 위에는 산타의 번호가 적혀있음
MATRIX = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(P):
    n, x, y = map(int, input().split())
    SANTA_POS[n] = [x-1, y-1]
    MATRIX[x-1][y-1] = n


# 상: 0 ~ 8방향
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def get_dis(x, y, x2, y2):
    return (x-x2)**2 + (y-y2)**2

# 충돌당한 산타의 번호와 새로 가려는 위치와 방향
# 해당 위치에 다른 산타 있으면 걔도 이동시켜야 함
def interaction(sid, nsx, nsy, d):
    global MATRIX
    new_matrix = [[0 for _ in range(N)] for _ in range(N)]
    new_matrix[nsx][nsy] = sid
    SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
    attacked_santa_id = MATRIX[nsx][nsy]

    while attacked_santa_id:
        MATRIX[nsx][nsy] = 0
        nsx, nsy = nsx+dx[d], nsy+dy[d]
        if in_range(nsx, nsy):
            new_matrix[nsx][nsy] = attacked_santa_id
            SANTA_POS[attacked_santa_id][0], SANTA_POS[attacked_santa_id][1] = nsx, nsy
            attacked_santa_id = MATRIX[nsx][nsy]
        else:
            GAME_OVER[attacked_santa_id] = True
            SANTA_POS[attacked_santa_id][0], SANTA_POS[attacked_santa_id][1] = nsx, nsy
            break
    
    for i in range(N):
        for j in range(N):
            if new_matrix[i][j] != 0:
                MATRIX[i][j] = new_matrix[i][j]


for turn in range(1, M+1):
    for i in range(P+1):
        if PASS_OUT[i] == turn:
            # print(turn, '턴에', i, '번 산타 부활')
            PASS_OUT[i] = False
    # === 1. 루돌프 이동 ===
    # 1) 제일 가까운 산타 선택
    min_dis = 1e9
    min_santa_num = -1
    min_santa_x = -1
    min_santa_y = -1
    for i in range(1, P+1):
        if GAME_OVER[i]:
            continue
        sx, sy = SANTA_POS[i]
        dis = get_dis(RX, RY, sx, sy)
        if dis < min_dis or (dis == min_dis and sx > min_santa_x) or (dis == min_dis and sx == min_santa_x and sy > min_santa_y):
            min_dis = dis
            min_santa_num = i
            min_santa_x = SANTA_POS[i][0]
            min_santa_y = SANTA_POS[i][1]
    # 2) 제일 가까운 산타를 향해 1칸 돌진
    dis_to_santa = 1e9
    nrx, nry = -1, -1
    move_dir = -1
    for i in range(8):
        nx, ny = RX+dx[i], RY+dy[i]
        if not in_range(nx, ny):
            continue
        dis = get_dis(nx, ny, min_santa_x, min_santa_y)
        if dis < dis_to_santa:
            dis_to_santa = dis
            nrx, nry = nx, ny
            dis_to_santa = dis
            move_dir = i
    RX, RY = nrx, nry
    # 만약 이 자리에 산타가 있다? => 충돌
    if MATRIX[RX][RY] > 0:
        # 충돌!
        # 충돌한 산타의 번호, 위치
        sid, sx, sy = MATRIX[RX][RY], SANTA_POS[MATRIX[RX][RY]][0], SANTA_POS[MATRIX[RX][RY]][1]
        PASS_OUT[sid] = turn+2
        SCORE[sid] += C
        MATRIX[sx][sy] = 0
        nsx, nsy = sx+dx[move_dir]*C, sy+dy[move_dir]*C
        # print(nsx, nsy)
        if not in_range(nsx, nsy):
            # 탈락
            GAME_OVER[sid] = True
            SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
        else:
            # 상호작용 가능성 있는지 확인
            if MATRIX[nsx][nsy] == 0:
                MATRIX[nsx][nsy] = sid
                SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
            else:
                # 상호작용 처리
                interaction(sid, nsx, nsy, move_dir)
    # print('루돌프 이동 후 MATRIX')
    # for _ in MATRIX:
    #     print(_)
    # print('루돌프 이동 후 SANTA_POS')
    # print(SANTA_POS)
    # print('루돌프 이동 후 위치', RX, RY)
    # === 2. 산타 이동 ===
    for sid in range(1, P+1):
        if not PASS_OUT[sid] and not GAME_OVER[sid]:
            # print(turn, '에', sid, '산타 간다')
            sx, sy = SANTA_POS[sid]
            dis_to_rudolph = 1e9
            move_dir = -1
            now_dis = get_dis(RX, RY, sx, sy)
            for i in range(0, 7, 2):
                nsx, nsy = sx+dx[i], sy+dy[i]
                if not in_range(nsx, nsy) or MATRIX[nsx][nsy] != 0:
                    continue
                dis = get_dis(nsx, nsy, RX, RY)
                if dis < now_dis and dis < dis_to_rudolph:
                    dis_to_rudolph = dis
                    move_dir = i
            # print(sid, '산타의', sx, sy, now_dis, dis_to_rudolph, move_dir)
            if move_dir != -1:
                # move_dir 방향으로 이동해야 함
                # 이동했는데 루돌프랑 만나면?
                MATRIX[sx][sy] = 0
                nsx, nsy = sx+dx[move_dir], sy+dy[move_dir]
                if not in_range(nsx, nsy):
                    GAME_OVER[sid] = True
                    SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
                    break
                if (nsx, nsy) != (RX, RY):
                    MATRIX[nsx][nsy] = sid
                    SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
                else:
                    # 충돌!
                    SCORE[sid] += D
                    PASS_OUT[sid] = turn+2
                    # 반대방향으로 이동
                    move_dir = (move_dir+4)%8
                    nsx, nsy = nsx+dx[move_dir]*D, nsy+dy[move_dir]*D
                    if not in_range(nsx, nsy):
                        GAME_OVER[sid] = True
                        SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
                    elif MATRIX[nsx][nsy] == 0:
                        MATRIX[sx][sy] = 0
                        MATRIX[nsx][nsy] = sid
                        SANTA_POS[sid][0], SANTA_POS[sid][1] = nsx, nsy
                    else: # 상호작용
                        # 충돌당한 산타의 번호와 새로 가려는 위치와 방향
                        interaction(sid, nsx, nsy, move_dir)
    for i in range(1, P+1):
        if GAME_OVER[i]:
            continue
        SCORE[i] += 1
    # if turn > 4:
    #     print(turn, '턴')
    #     print('점수', SCORE)
    #     print('루돌프 위치', RX, RY)
    #     print('산타 이동 후 MATRIX')
    #     for _ in MATRIX:
    #         print(_)
    #     print('산타 이동 후 SANTA_POS')
    #     print(SANTA_POS)
    #     print('산타 이동 후 루돌프 위치', RX, RY)

for i in range(1, P+1):
    print(SCORE[i], end = ' ')