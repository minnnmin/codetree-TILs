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

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# m개씩 짝지어진 병원들 정보. m이 2일 때: [(병원1 위치, 병원2 위치), ... ]
SELECTED_HOSPITALS = []

def backtracking(n, history):
    global SELECTED_HOSPITALS 

    if n == M:
        tmp = [HOSPITALS[i] for i in history]
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
    # pairs에 병원 m개 담겨있음
    res = 0
    for x, y in PEOPLE:
        tmp = 1e9 # 이번 사람의 최소 병원거리
        for hx, hy in pairs:
            tmp2 = abs(hx-x) + abs(hy-y)
            tmp = tmp2 if tmp2 < tmp else tmp
        res += tmp
    ANSWER = res if res < ANSWER else ANSWER
    for x, y in pairs:
        MATRIX[x][y] = 0

print(ANSWER)