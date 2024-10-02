# L 체스판 크기, N 기사의 수, Q 명령의 수
L, N, Q = map(int, input().split())
TRAP_AND_WALL = [list(map(int, input().split())) for _ in range(L)]

# (r,c,h,w,k); 기사의 처음 위치 (r,c)를 좌측 상단 꼭지점으로 하며
# 세로 길이가 h, 가로 길이가 w인 직사각형 형태를 띄고 있으며 초기 체력이 k
KNIGHT_POS = [()]

for _ in range(N):
    r, c, h, w, k = map(int, input().split())
    KNIGHT_POS.append([r-1, c-1, h, w, k, k]) # 맨 뒤 k는 기존값 보존을 위함
# for _ in KNIGHT_POS:
#     print(_)

KNIGHT_STATE = [[0 for _ in range(L)] for _ in range(L)]
for i, (r, c, h, w, k, origin_k) in enumerate(KNIGHT_POS[1:]):
    for x in range(r, r+h):
        for y in range(c, c+w):
            KNIGHT_STATE[x][y] = i+1

ORDER = [tuple(map(int, input().split())) for _ in range(Q)]
# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(x, y):
    return -1 < x < L and -1 < y < L

ATTACKED = []
# i번 기사를 d방향으로 한칸 밀 수 있는지 확인
def can_move(knight_num, d):
    global ATTACKED
    attacked = [knight_num] # 밀려난 애들 여기 임시로 저장
    history = [knight_num] # 이동해야 하는 애들 모두 저장

    while attacked:
        now_knight_num = attacked.pop()
        r, c, h, w, k, origin_k = KNIGHT_POS[now_knight_num]
        # d방향으로 이동한 뒤 왼쪽 위 꼭짓점은 nx, ny
        # nx, ny로 부터 시작하는 사각형을 점검해보고 범위 내 and 벽 아니면 이동 가능
        # 이 때 다른 번호 만나도 되긴 하는데 걔도 이동 시켜야 돼
        r, c = r + dx[d], c + dy[d]
        for x in range(r, r+h):
            for y in range(c, c+w):
                if not in_range(x, y) or TRAP_AND_WALL[x][y] == 2:
                    return False
                else:
                    if 0 < KNIGHT_STATE[x][y] and KNIGHT_STATE[x][y] != now_knight_num:
                        if KNIGHT_STATE[x][y] not in attacked:
                            attacked.append(KNIGHT_STATE[x][y])
                        if KNIGHT_STATE[x][y] not in history:
                            history.append(KNIGHT_STATE[x][y])
    
    # can_push 함수 리턴값이 True면, 이동가능하다는 거고, 전역변수인 ATTACKED가 갱신되어 있을 것(없을 수도 있음. 혼자만 이동한 경우)
    ATTACKED = history
    return True


# 체력 0돼서 죽은 기사 번호
DEAD_KNIGHT = []


# i번 기사를 d방향으로 한칸 이동, 그때 밀려나는 애들도 모두 이동
def move(d):
    global ATTACKED, KNIGHT_POS, KNIGHT_STATE, DEAD_KNIGHT # 기사들 위치도 갱신

    # 기존 거 지워
    for knight_num in ATTACKED:
        r, c, h, w, k, origin_k = KNIGHT_POS[knight_num]
        for x in range(r, r+h):
            for y in range(c, c+w):
                KNIGHT_STATE[x][y] = 0

    # 새로 갱신
    for knight_num in ATTACKED:
        damage = 0
        r, c, h, w, k, origin_k = KNIGHT_POS[knight_num]
        r, c = r + dx[d], c + dy[d]
        # 데미지 먼저 세 - 명령 받은 얘 제외
        if knight_num != ATTACKED[0]:
            for x in range(r, r+h):
                for y in range(c, c+w):
                    if TRAP_AND_WALL[x][y] == 1:
                        damage += 1
            if damage >= KNIGHT_POS[knight_num][4]:
                # 죽음
                DEAD_KNIGHT.append(knight_num)
                KNIGHT_POS[knight_num] = []
                continue

        # 죽진 않는다는 거니까 위치랑 값 모두 갱신
        KNIGHT_POS[knight_num][0] = r
        KNIGHT_POS[knight_num][1] = c
        for x in range(r, r+h):
            for y in range(c, c+w):
                KNIGHT_STATE[x][y] = knight_num
                if TRAP_AND_WALL[x][y] == 1 and knight_num != ATTACKED[0]:
                    KNIGHT_POS[knight_num][4] -= 1


t = 0
for knight_num, d in ORDER:
    t += 1
    if knight_num in DEAD_KNIGHT:
        continue
    if can_move(knight_num, d):
        move(d)
    else:
        continue

answer = 0
for i in range(1, len(KNIGHT_POS)):
    if i not in DEAD_KNIGHT:
        r, c, h, w, k, origin_k = KNIGHT_POS[i]
        answer += origin_k-k

print(answer)