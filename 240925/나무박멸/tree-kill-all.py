N, M, K, C = map(int, input().split())
TREES = [list(map(int, input().split())) for _ in range(N)]
TMP_TREES = [[0 for _ in range(N)] for _ in range(N)] # 번식한 나무 개수 임시 저장용
KILLER = [[0 for _ in range(N)] for _ in range(N)] # 0이면 없는 거고, 있으면 남은 년 수가 저장됨
KILLED_TREE = 0

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


# 대각선: 좌상, 우상, 좌하, 우하
da = [-1, -1, 1, 1]
db = [-1, 1, -1, 1]

# (x, y) 위치의 나무를 기준으로, 상하좌우에 나무가 몇개 있는지 리턴
def adj_tree_cnt(x, y):
    res = 0

    for i in range(4):
        new_x = x + dx[i]
        new_y = y + dy[i]
        if -1 < new_x < N and -1 < new_y < N and TREES[new_x][new_y] > 0:
            res += 1
    
    return res


# 나무 성장
def grow_trees():
    global TREES
    for i in range(N):
        for j in range(N):
            if TREES[i][j] > 0: # 나무가 있다면,
                TREES[i][j] += adj_tree_cnt(i, j)


# (x, y) 위치의 나무를 기준으로, 상하좌우 중 어느 곳에 번식할 수 있는지 리스트로 리턴
# 리턴값이 [0, 1, 2, 3]면 상, 하, 좌, 우 4곳에 모두 번식 가능
def make_baby_trees_pos(x, y):
    res = []

    for i in range(4):
        new_x = x + dx[i]
        new_y = y + dy[i]
        if -1 < new_x < N and -1 < new_y < N and TREES[new_x][new_y] == 0 and KILLER[new_x][new_y] == 0:
            res.append(i)

    return res


# 나무 번식
def make_baby_trees():
    global TMP_TREES, TREES
    for i in range(N):
        for j in range(N):
            if TREES[i][j] > 0:
                baby_trees_pos = make_baby_trees_pos(i, j)
                for pos in baby_trees_pos:
                    ni = i + dx[pos]
                    nj = j + dy[pos]
                    TMP_TREES[ni][nj] += TREES[i][j] // len(baby_trees_pos)
    

    # TREES 갱신, TMP_TREES 초기화
    for i in range(N):
        for j in range(N):
            TREES[i][j] += TMP_TREES[i][j]
            TMP_TREES[i][j] = 0
    

# (x, y) 위치에서 제초제를 뿌린 경우, 죽는 나무의 수를 리턴
def how_many_trees_killed(x, y):
    killed_trees = TREES[x][y] # 제초제 뿌린 위치 나무 수

    for d in range(4):
        for i in range(1, K+1):
            new_x = x + i*da[d]
            new_y = y + i*db[d]
            if -1 < new_x < N and -1 < new_y < N and TREES[new_x][new_y] > 0:
                killed_trees += TREES[new_x][new_y]
            else:
                break

    return killed_trees


# (x, y) 위치에서 제초제 분사.
def do_kill(x, y):
    global KILLER, KILLED_TREE

    # 자기 자신
    KILLED_TREE += TREES[x][y]
    TREES[x][y] = 0
    KILLER[x][y] = C
    
    for d in range(4):
        for i in range(1, K+1):
            new_x = x + i*da[d]
            new_y = y + i*db[d]
            if -1 < new_x < N and -1 < new_y < N and TREES[new_x][new_y] > -1:
                if TREES[new_x][new_y] == 0:
                    KILLER[new_x][new_y] = C
                    break
                KILLED_TREE += TREES[new_x][new_y]
                TREES[new_x][new_y] = 0
                KILLER[new_x][new_y] = C
            else:
                break


# 제초제 뿌리기 - 나무 있는 칸에 뿌려라. (제초제 없는 곳도 ㄴㄴ 어차피 거기 나무 0개)
def kill_trees():
    # 박멸 나무 수가 최대인 곳 찾기
    max_dead_trees = 0
    killer_pos = []
    for i in range(N):
        for j in range(N):
            if TREES[i][j] > 0:
                tmp = how_many_trees_killed(i, j)
                if tmp > max_dead_trees:
                    max_dead_trees = tmp
                    killer_pos = [i, j]
    
    # 실제로 분사하면서 나무 수 0으로 초기화, KILLER 배열에 잔여 년 추가
    if killer_pos:
        do_kill(killer_pos[0], killer_pos[1])


# KILLER 에서 남은 년 수 1씩 차감
def update_year():
    global KILLER
    for i in range(N):
        for j in range(N):
            if KILLER[i][j] > 0:
                KILLER[i][j] -= 1


for m in range(M):
    grow_trees()
    make_baby_trees()
    kill_trees()
    if m != 0:
        update_year()

print(KILLED_TREE)


# grow_trees()
# make_baby_trees()
# do_kill(2, 3)
# for _ in TREES:
#     print(_)
# print()
# for _ in KILLER:
#     print(_)