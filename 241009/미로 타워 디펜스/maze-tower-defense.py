N, M = map(int, input().split())

MATRIX = [list(map(int, input().split())) for _ in range(N)]

# 해당 자리에서는 어떻게 움직여야 하는지
DIR_MATRIX = [[-1 for _ in range(N)] for _ in range(N)]

# (공격방향, 공격칸수)
ORDER = [list(map(int, input().split())) for _ in range(M)]

# 우, 하, 좌, 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

X, Y, D = 0, 0, 0
x, y = 0, 0

NUM_LIST = [3]
for _ in range(N-3):
    NUM_LIST.append(2)
NUM_LIST.append(1)

NUM_LIST2 = NUM_LIST[::-1]

for move_cnt, dir_cnt in zip(range(N-1, 0, -1), NUM_LIST):
    for _ in range(dir_cnt):
        for i in range(move_cnt):
            nx, ny = x+dx[D], y+dy[D]
            # 자 이제 nx, ny를 최대한 앞으로 땡기는 거야
            # 어떻게? 그 자리에 있는 방향대로
            # print(nx, ny)
            DIR_MATRIX[x][y] = D
            x, y = nx, ny
        D = (D+1)%4
# DIR_MATRIX[N//2][N//2-1] = 0

def move():
    global MATRIX
    X, Y, D = N//2, N//2-1, 1
    now_x, now_y = N//2, N//2-1
    for move_cnt, dir_cnt in zip(range(1, N), NUM_LIST2):
        for _ in range(dir_cnt):
            for i in range(move_cnt):
                now_x, now_y = now_x+dx[D], now_y+dy[D]
                move_d = DIR_MATRIX[now_x][now_y]
                nx, ny = now_x, now_y
                while move_d != -1:
                    move_d = DIR_MATRIX[nx][ny]
                    new_x, new_y = nx+dx[move_d], ny+dy[move_d]
                    if MATRIX[new_x][new_y] > 0:
                        break
                    # 이동하려는 자리에 몬스터 없으면 옮겨
                    MATRIX[new_x][new_y] = MATRIX[nx][ny]
                    MATRIX[nx][ny] = 0
                    nx, ny = new_x, new_y
            D = (D-1)%4


def in_range(x, y):
    return -1 < x < N and -1 < y < N


from collections import deque

q = deque()

def del_monsters():
    global MATRIX, SCORE
    # 안에서부터 나오면서 검사하다가 0 만나면 끝내
    X, Y, D = N//2, N//2-1, 1
    now_x, now_y = N//2, N//2-1
    now_monster = MATRIX[now_x][now_y]
    cnt = 1
    group = [(now_x, now_y)]
    deleted = False
    for move_cnt, dir_cnt in zip(range(1, N), NUM_LIST2):
        for _ in range(dir_cnt):
            for i in range(move_cnt):
                now_x, now_y = now_x+dx[D], now_y+dy[D]
                if MATRIX[now_x][now_y] == now_monster:
                    cnt += 1
                    group.append((now_x, now_y))
                elif MATRIX[now_x][now_y] > 0:
                    if cnt >= 4:
                        SCORE += now_monster*cnt
                        for x, y in group:
                            MATRIX[x][y] = 0
                        deleted = True
                    now_monster = MATRIX[now_x][now_y]
                    cnt = 1
                    group = [(now_x, now_y)]
                elif MATRIX[now_x][now_y] == 0:
                    if cnt >= 4:
                        SCORE += now_monster*cnt
                        for x, y in group:
                            MATRIX[x][y] = 0
                        deleted = True
                    return deleted
                move_d = DIR_MATRIX[now_x][now_y]
            D = (D-1)%4
    if cnt >= 4:
        SCORE += now_monster*cnt
        for x, y in group:
            MATRIX[x][y] = 0
        deleted = True
    return deleted


# 남은 걸로 수열 만들기
def get_seq():
    seq = [] # (개수, 숫자)

    X, Y, D = N//2, N//2-1, 1
    now_x, now_y = N//2, N//2-1
    now_monster = MATRIX[now_x][now_y]
    cnt = 1
    for move_cnt, dir_cnt in zip(range(1, N), NUM_LIST2):
        for _ in range(dir_cnt):
            for i in range(move_cnt):
                now_x, now_y = now_x+dx[D], now_y+dy[D]
                if MATRIX[now_x][now_y] == 0:
                    seq.append(cnt)
                    seq.append(now_monster)
                    return seq
                elif MATRIX[now_x][now_y] == now_monster:
                    cnt += 1
                elif MATRIX[now_x][now_y] != now_monster:
                    seq.append(cnt)
                    seq.append(now_monster)
                    now_monster = MATRIX[now_x][now_y]
                    cnt = 1
            D = (D-1)%4
    seq.append(cnt)
    seq.append(now_monster)
    return seq


SCORE = 0
for attack_d, cnt in ORDER:
    cx, cy = N//2, N//2
    ''' 1. 공격 '''
    for i in range(cnt):
        ncx, ncy = cx+dx[attack_d], cy+dy[attack_d]
        SCORE += MATRIX[ncx][ncy]
        MATRIX[ncx][ncy] = 0
        cx, cy = ncx, ncy

    move()

    while True:
        ''' 3. 연속 4개이상 만나는 숫자 동시 삭제 '''
        deleted = del_monsters()
        if not deleted:
            break
        move()

    ''' 4. 남은 거 다시 넣기 '''
    seq = get_seq()
    l = len(seq)
    now_x, now_y, D = N//2, N//2-1, 1
    MATRIX[now_x][now_y] = seq[0]
    seq_id = 1
    DIR_MATRIX[N//2][N//2-1] = 0
    for move_cnt, dir_cnt in zip(range(1, N), NUM_LIST2):
        for _ in range(dir_cnt):
            for i in range(move_cnt):
                if seq_id == l:
                    break
                now_x, now_y = now_x+dx[D], now_y+dy[D]
                MATRIX[now_x][now_y] = seq[seq_id]
                seq_id += 1
            D = (D-1)%4
    DIR_MATRIX[N//2][N//2-1] = -1
    
    # break
print(SCORE)