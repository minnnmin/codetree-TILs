import heapq

Q = int(input())

tmp = list(map(int, input().split()))
N, M, P = tmp[1], tmp[2], tmp[3]
# MATRIX = [[0 for i in range(M)] for _ in range(N)]


# 토끼 선정용
RABBIT1 = []
# 점수만 별도 저장
SCORE = {}

for i in range(4, len(tmp), 2):
    # [점프횟수, 행+열, 행, 열, pid, d]
    heapq.heappush(RABBIT1, [0, 0, 0, 0, tmp[i], tmp[i+1]])
    SCORE[tmp[i]] = 0


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
    global RABBIT1
    cnt, rc, origin_r, origin_c, pid, dis = heapq.heappop(RABBIT1)

    next_pos = []

    for d in range(4): # d번 돌아보기
        # d는 상우하좌 중 하나
        r, c = origin_r, origin_c
        if d % 2 == 0:
            ndis = dis % (2*(N-1))
        else:
            ndis = dis % (2*(M-1))
        for i in range(ndis):
            nr, nc = r+dx[d], c+dy[d]
            if not in_range(nr, nc):
                d = change_dir(d)
                nr, nc = r+dx[d], c+dy[d]
            r, c = nr, nc
        next_pos.append((r, c))
    
    next_pos.sort(key = lambda x: (-(x[0]+x[1]), -x[0], -x[1]))
    nr, nc = next_pos[0]
    heapq.heappush(RABBIT1, [cnt+1, nr+nc, nr, nc, pid, dis])
    return pid, nr+nc


def move_rabbit1():
    # 200 명령에서 사용
    # 상하좌우로 d만큼 이동시켜보고 우선순위 높은 거 선택해서 이동 
    global RABBIT1
    cnt, rc, origin_r, origin_c, pid, dis = heapq.heappop(RABBIT1)

    next_pos = []
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
    heapq.heappush(RABBIT1, [cnt+1, nr+nc, nr, nc, pid, dis])
    return pid, nr+nc

for order in ORDER:
    if order[0] == 200:
        K, S = order[1], order[2]
        for _ in range(K):
            # 토끼 한마리 골라 이동
            pid, rc = move_rabbit()
            # 나머지 토끼들 rc점 획득
            for i in SCORE:
                if i != pid:
                    SCORE[i] += rc+2
        # 우선순위 높은 토끼 골라 S점 추가
        # 토끼 찾기
        nrc, nr, nc, npid = 0, 0, 0, 0
        for cnt, rc, r, c, pid, dis in RABBIT1:
            if cnt == 0:
                continue
            if rc > nrc:
                nrc, nr, nc, npid = rc, r, c, pid
            elif rc == nrc and r > nr:
                nrc, nr, nc, npid = rc, r, c, pid
            elif rc == nrc and r == nr and c > nc:
                nrc, nr, nc, npid = rc, r, c, pid
            elif rc == nrc and r == nr and c == nc and pid > npid:
                nrc, nr, nc, npid = rc, r, c, pid
        # S점 추가
        for i in range(len(RABBIT1)):
            cnt, rc, r, c, pid, dis = RABBIT1[i]
            if pid == npid:
                SCORE[pid] += S
                break
        # print('200후 점수')
        # print(SCORE)
    elif order[0] == 300:        
        pid_t, L = order[1], order[2]
        # pid가 pid_t인 토끼의 dis를 L배
        for i in range(len(RABBIT1)):
            cnt, rc, r, c, pid, dis = RABBIT1[i]
            if pid == pid_t:
                RABBIT1[i][5] *= L
                break
    elif order[0] == 400:
        break
# print(RABBIT1)
# print(SCORE)

# 토끼 최대 점수 출력
ANSWER = 0
for pid in SCORE:
    if SCORE[pid] > ANSWER:
        ANSWER = SCORE[pid]
print(ANSWER)