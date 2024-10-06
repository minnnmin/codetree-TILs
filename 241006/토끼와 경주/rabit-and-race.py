Q = int(input())

tmp = list(map(int, input().split()))
N, M, P = tmp[1], tmp[2], tmp[3]
# MATRIX = [[0 for i in range(M)] for _ in range(N)]

RABBIT = []
# [0, 0, 0, 0, 10, 0, 2]
# [0, 0, 0, 0, 20, 0, 5]
for i in range(4, len(tmp), 2):
    # [점프횟수, 행+열, 행, 열, pid, 점수, d]
    RABBIT.append([0, 0, 0, 0, tmp[i], 0, tmp[i+1]])

ORDER = [list(map(int, input().split())) for _ in range(Q-1)]

# 상우하좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(x, y):
    return -1 < x < N and -1 < y < M

# 0과 2, 1과 3
def change_dir(d):
    return (d+2)%4

def move_rabbit():
    # 200 명령에서 사용
    # 상하좌우로 d만큼 이동시켜보고 우선순위 높은 거 선택해서 이동 
    global RABBIT
    cnt, rc, origin_r, origin_c, pid, score, dis = RABBIT[0]
    next_pos = []
    # 상
    for d in range(4): # d번 돌아보기
        # d는 상우하좌 중 하나
        r, c = origin_r, origin_c
        for i in range(dis):
            nr, nc = r+dx[d], c+dy[d]
            if not in_range(nr, nc):
                d = change_dir(d)
                nr, nc = r+dx[d], c+dy[d]
            r, c = nr, nc
        next_pos.append((r, c))
    
    next_pos.sort(key = lambda x: (-(x[0]+x[1]), -x[0], -x[1]))
    nr, nc = next_pos[0]
    RABBIT[0][0] += 1
    RABBIT[0][1], RABBIT[0][2], RABBIT[0][3] = nr+nc, nr, nc 
    # print('RABBIT[0]', RABBIT[0])
    return nr+nc

for order in ORDER:
    if order[0] == 200:
        K, S = order[1], order[2]
        for _ in range(K):
            # 토끼 한마리 골라 이동
            RABBIT.sort()
            rc = move_rabbit()
            # 나머지 토끼들 rc점 획득
            for i in range(1, len(RABBIT)):
                RABBIT[i][5] += rc+2
        # 우선순위 높은 토끼 골라 S점 추가
        RABBIT.sort(key = lambda x: (-x[1], -x[2], -x[3], -x[4], -x[0]))
        if RABBIT[0][0] != 0:
            RABBIT[0][5] += S
    if order[0] == 300:
        pid_t, L = order[1], order[2]
        # pid가 pid_t인 토끼의 dis를 L배
        for i in range(len(RABBIT)):
            if RABBIT[i][4] == pid_t:
                RABBIT[i][6] *= L
    if order[0] == 400:
        break

# 토끼 최대 점수 출력
ANSWER = 0
for i in range(len(RABBIT)):
    if RABBIT[i][5] > ANSWER:
        ANSWER = RABBIT[i][5]

print(ANSWER)