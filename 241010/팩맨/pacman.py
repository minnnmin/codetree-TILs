M, T = map(int, input().split())
px, py = map(int, input().split())
PACKMAN_POS = (px-1, py-1)

# 각 위치에 있는 알의 방향들이 저장
EGG = [[[] for _ in range(4)] for _ in range(4)]
# 각 위치에서 죽은 시체들이 소멸되는 턴이 저장
DEAD = [[[] for _ in range(4)] for _ in range(4)]
# 각 위치에 있는 몬스터 [위~ 반시계 방향] 각 방향을 갖는 몬스터 수
MONSTER = [[[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(4)] for _ in range(4)]

for _ in range(M):
    r, c, d = map(int, input().split())
    MONSTER[r-1][c-1][d-1] += 1

# 위~ 반시계
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

def in_range(x, y):
    return -1 < x < 4 and -1 < y < 4

from collections import deque

q = deque()

def packman_move():
    # 팩맨 이동: 64 경로 모두 이동해보면서, 몬스터를 최대로 먹으면서 우선순위 높은 이동한 경로 찾아내기

    px, py = PACKMAN_POS
    get_monster = 0
    history = [7]

    for d1 in range(0, 8, 2):
        for d2 in range(0, 8, 2):
            for d3 in range(0, 8, 2):
                px, py = PACKMAN_POS
                # d1->d2->d3 순으로 이동
                CAN_GO = True
                monster = 0
                history_pos = []
                for d in [d1, d2, d3]:
                    px, py = px+dx[d], py+dy[d]
                    if (px, py) in history_pos: # 재방문 방지
                        break
                    if not in_range(px, py):
                        CAN_GO = False
                        break
                    if sum(MONSTER[px][py]) > 0:
                        # 그 자리 몬스터가 있다면
                        monster += sum(MONSTER[px][py])
                    history_pos.append((px, py))
                if CAN_GO:
                    if monster > get_monster or (monster == get_monster and [d1, d2, d3] < history):
                        get_monster = monster
                        history = [d1, d2, d3]
    
    return get_monster, history                    



for turn in range(T):
    ''' 1. 몬스터 복제 '''
    for i in range(4):
        for j in range(4):
            for d in range(8):
                if MONSTER[i][j][d] > 0:
                    EGG[i][j].append(d)

    ''' 2. 몬스터 이동 '''
    new_monster = [[[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            for d in range(8):
                member_cnt = MONSTER[x][y][d]
                if member_cnt == 0:
                    continue
                for _ in range(7): # 가능할 때까지 방향 바꿔보기
                    nx, ny = x+dx[d], y+dy[d]
                    if in_range(nx, ny) and sum(DEAD[nx][ny]) == 0 and (nx, ny) != PACKMAN_POS:
                        new_monster[nx][ny][d] += member_cnt # 멤버 수만큼 갱신
                        break
                    d = (d+1)%8
    # 모든 몬스터 이동 후 new_monster -> MONTSER에 덮어쓰기
    MONSTER = new_monster
    ''' 3. 팩맨 이동 '''
    get_monster, history = packman_move()
    px, py = PACKMAN_POS
    # 해당 루트 돌면서 만나는 몬스터를 시체로 만들 것
    if get_monster > 0:
        for d in history:
            px, py = px+dx[d], py+dy[d]
            if sum(MONSTER[px][py]) > 0:
                DEAD[px][py].append(turn+2)
                MONSTER[px][py] = [0, 0, 0, 0, 0, 0, 0, 0]
    PACKMAN_POS = (px, py)
    ''' 4. 몬스터 시체 소멸 '''
    for i in range(4):
        for j in range(4):
            remain = []
            for t in DEAD[i][j]:
                if t != turn:
                    remain.append(t)
            DEAD[i][j] = remain
    
    ''' 5. 몬스터 복제(알들이 깨어남) '''
    for i in range(4):
        for j in range(4):
            for d in EGG[i][j]:
                MONSTER[i][j][d] += 1
            EGG[i][j] = []

    # for _ in MONSTER:
    #     print(_)
survive = 0
for i in range(4):
    for j in range(4):
        survive += sum(MONSTER[i][j])

print(survive)