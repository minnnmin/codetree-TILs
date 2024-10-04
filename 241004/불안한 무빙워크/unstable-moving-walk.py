N, K = map(int, input().split())

MOVING_WALK = [[i for i in range(1, N+1)], [i for i in range(N*2, N, -1)]]
num = 1
PEOPLE = [0 for _ in range(N)]
STABLE = [-1] + list(map(int, input().split())) # 0번째 판은 안 씀


# 무빙워크 회전(그 위에 있는 사람도 같이 이동)
def rotate():
    global MOVING_WALK, PEOPLE

    # 무빙워크 회전 - 각 판에는 번호가 쓰여있다
    tmp = MOVING_WALK[0][N-1]
    for j in range(N-1, 0, -1):
        MOVING_WALK[0][j] = MOVING_WALK[0][j-1]
    MOVING_WALK[0][0] = MOVING_WALK[1][0]
    for j in range(N-1):
        MOVING_WALK[1][j] = MOVING_WALK[1][j+1]
    MOVING_WALK[1][N-1] = tmp

    # 사람도 동일하게 회전
    for j in range(N-1, 0, -1):
        PEOPLE[j] = PEOPLE[j-1]
    PEOPLE[0] = 0
    PEOPLE[-1] = 0 # N칸에 도착한 사람 바로 하차


# 사람 추가
def add_people():
    global PEOPLE

    if PEOPLE[0] == 0 and STABLE[MOVING_WALK[0][0]] > 0:
        PEOPLE[0] = 1
        STABLE[MOVING_WALK[0][0]] -= 1


# 이동할 수 있는 사람 이동 - 안정성 갱신
def move_people():
    global PEOPLE, STABLE
    for j in range(N-1, 0, -1):
        if PEOPLE[j-1] == 1 and PEOPLE[j] == 0 and STABLE[MOVING_WALK[0][j]] > 0:
            PEOPLE[j] = 1
            PEOPLE[j-1] = 0
            STABLE[MOVING_WALK[0][j]] -= 1
    PEOPLE[-1] = 0 # N칸에 사람 있으면 하차 시키기

      
KEEP_GOING = True
turn = 1
rotate()
add_people()
if STABLE.count(0) >= K:
    KEEP_GOING = False

while KEEP_GOING:
    turn += 1
    rotate()
    move_people()
    add_people()
    if STABLE.count(0) >= K:
        break

print(turn)