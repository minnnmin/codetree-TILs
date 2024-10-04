N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]
HOSPITALS = []
PEOPLE = []

for x in range(N):
    for y in range(N):
        if MATRIX[x][y] == 2:
            HOSPITALS.append((x, y))
            MATRIX[x][y] = 0
        elif MATRIX[x][y] == 1:
            PEOPLE.append((x, y))

L = len(HOSPITALS)
ANSWER = 1e9

from collections import deque

q = deque()

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def bfs(x, y):
    # (x, y)에 있는 사람의 최소 병원거리
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[x][y] = True
    q.append((x, y, 0))

    while q:
        r, c, dis = q.popleft()
        dis += 1
        for i in range(4):
            nr, nc = r+dx[i], c+dy[i]
            if in_range(nr, nc) and not visited[nr][nc]:
                if MATRIX[nr][nc] == 2: # 병원 발견
                    q.clear()
                    return dis
                else:
                    visited[nr][nc] = True
                    q.append((nr, nc, dis))

    return 'err' # 이게 출력되면 안됨


# 현재 MATRIX 기준으로 병원거리 합 리턴
def get_hospital_dist():
    global ANSWER
    res = 0
    for x, y in PEOPLE:
        q.clear()
        tmp = bfs(x, y)
        res += tmp
                
    ANSWER = res if res < ANSWER else ANSWER


# history에는 이미 선택된 병원의 인덱스가 들어있음. 이것들보다 큰 것만 추가 가능
def backtracking2(n, history):
    global ANSWER 

    if n == M:
        res = get_hospital_dist()
        ANSWER = res if res < ANSWER else ANSWER
        return

    for new_pos_id in range(L):
        if not history or new_pos_id > history[-1]:
            history.append(new_pos_id)
            nx, ny = HOSPITALS[new_pos_id]
            MATRIX[nx][ny] = 2
            backtracking(n+1, history)
            MATRIX[nx][ny] = 0
            history.pop()


# m개씩 짝지어진 병원들 정보. m이 2일 때: [(병원1 위치, 병원2 위치), ... ]
SELECTED_HOSPITALS = []

def backtracking(n, history):
    global SELECTED_HOSPITALS 

    if n == M:
        tmp = []
        for i in history:
            tmp.append(HOSPITALS[i])
        SELECTED_HOSPITALS.append(tmp)
        return

    for new_pos_id in range(L):
        if not history or new_pos_id > history[-1]:
            history.append(new_pos_id)
            nx, ny = HOSPITALS[new_pos_id]
            backtracking(n+1, history)
            history.pop()

backtracking(0, []) # -> 남겨둘 병원 쌍이 저장되어 있음

for pairs in SELECTED_HOSPITALS:
    for x, y in pairs:
        MATRIX[x][y] = 2
    res = 0
    for x, y in PEOPLE:
        # q.clear()
        tmp = bfs(x, y)
        res += tmp
    
    ANSWER = res if res < ANSWER else ANSWER
    for x, y in pairs:
        MATRIX[x][y] = 0

print(ANSWER)