from collections import deque

N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]
ANSWER = 0 # 점수 총합

# 주사위 정보 (초기의 상태로 초기화)
DICE = [1, 6, 4, 3, 2, 5]
DICE_POS = [0, 0]

# 이동 방향 (초기 방향으로 초기화)
DIR = 1

# 상, 우, 하, 좌 순으로 0~3
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

# 주사위 굴리기
def move_dice():
    # DIR: 0~3
    global DICE

    if DIR == 0: # 위로 이동
        DICE = [DICE[4], DICE[5], DICE[2], DICE[3], DICE[1], DICE[0]]
    elif DIR == 1: # 오른쪽으로 이동
        DICE = [DICE[2], DICE[3], DICE[1], DICE[0], DICE[4], DICE[5]]
    elif DIR == 2: # 아래로 이동
        DICE = [DICE[5], DICE[4], DICE[2], DICE[3], DICE[0], DICE[1]]
    elif DIR == 3: # 왼쪽으로 이동
        DICE = [DICE[3], DICE[2], DICE[0], DICE[1], DICE[4], DICE[5]]
    
q = deque()

# 점수 계산하기
def bfs():
    # q에 DICE_POS가 들어있음
    global ANSWER, q

    num = MATRIX[DICE_POS[0]][DICE_POS[1]]
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[DICE_POS[0]][DICE_POS[1]] = True
    cnt = 1

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if in_range(nx, ny) and not visited[nx][ny] and MATRIX[nx][ny] == num:
                cnt += 1
                visited[nx][ny] = True
                q.append((nx, ny))

    ANSWER += cnt*num

for _ in range(M):
    nx, ny = DICE_POS[0] + dx[DIR], DICE_POS[1] + dy[DIR]
    if not in_range(nx, ny):
        DIR = abs((DIR+2)%4)
        nx, ny = DICE_POS[0] + dx[DIR], DICE_POS[1] + dy[DIR]
    move_dice() # 주사위 굴림
    DICE_POS = [nx, ny]
    q.append(DICE_POS)
    bfs()
    if DICE[1] > MATRIX[DICE_POS[0]][DICE_POS[1]]:
        # DIR을 시계방향 회전
        DIR = (DIR+1)%4
    elif DICE[1] < MATRIX[DICE_POS[0]][DICE_POS[1]]:
        # DIR을 반시계방향 회전
        DIR = (DIR+3)%4
    # 똑같으면 방향 전환 안함
    # print(DICE)
    # print(DICE_POS)
    # print(DIR)
    # print(ANSWER)

print(ANSWER)