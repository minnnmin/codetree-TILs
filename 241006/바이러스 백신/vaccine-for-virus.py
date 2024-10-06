N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]
HOSPITALS = [] # HOSPITALS[i]는 i번 병원의 좌표
for i in range(N):
    for j in range(N):
        if MATRIX[i][j] == 2:
            HOSPITALS.append((i, j))
L = len(HOSPITALS)
SELECTED_HOSPITAL_PAIRS = []

# 이 백트래킹 돌려서 selected_hospital_pairs를 갱신
def backtracking(n, history):
    global SELECTED_HOSPITAL_PAIRS
    
    if n == M:
        SELECTED_HOSPITAL_PAIRS.append(history)
        return
    
    for i in range(L):
        if not history or history[-1] < i:
            backtracking(n+1, history + [i])


from collections import deque
q = deque()

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def bfs(x, y):
    global MIN_DIS_MATRIX
    dis = 0
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[x][y] = True
    q.append((x, y, 0))

    while q:
        r, c, dis = q.popleft()
        for i in range(4):
            nr, nc = r+dx[i], c+dy[i]
            if in_range(nr, nc) and not visited[nr][nc] and MATRIX[nr][nc] != 1\
                and MIN_DIS_MATRIX[nr][nc] > dis+1:
                q.append((nr, nc, dis+1))
                visited[nr][nc] = True
                MIN_DIS_MATRIX[nr][nc] = dis+1

backtracking(0, [])
ANSWER = 1e9 # 모든 바이러스를 없애는 데 걸린 최소 시간 (이게 2500이면 제거 못한 거)
# 백트 돌고 나면 SELECTED_HOSPITAL_PAIRS 세팅 완료
for pairs in SELECTED_HOSPITAL_PAIRS:
    MIN_DIS_MATRIX = [[1e9 for _ in range(N)] for _ in range(N)]
    for hospital_num in pairs:
        x, y = HOSPITALS[hospital_num]
        # 각 병원에 대해서는 최소 거리를 0으로 세팅해 놔야 함
        MIN_DIS_MATRIX[x][y] = 0
        bfs(x, y) # MIN_DIS_MATRIX 위에, 벽이 없는 길만 검사하면서 최소 이동 거리 갱신
    # for _ in MIN_DIS_MATRIX:
    #     print(_)
    # print()
    # 자 이제 제거되지 않은 바이러스 있는지 확인
    # =============== 여기 할 차례 =======
    max_dis = 0
    for i in range(N):
        for j in range(N):
            if MATRIX[i][j] == 0:
                max_dis = MIN_DIS_MATRIX[i][j] if max_dis < MIN_DIS_MATRIX[i][j] else max_dis
    # print('max', max_dis)
    ANSWER = max_dis if max_dis < ANSWER else ANSWER
    # print('ANSWER', ANSWER)

if ANSWER == 1e9:
    ANSWER = -1
print(ANSWER)