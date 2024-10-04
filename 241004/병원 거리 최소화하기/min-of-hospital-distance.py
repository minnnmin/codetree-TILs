N, M = map(int, input().split())
MATRIX = [list(map(int, input().split())) for _ in range(N)]
HOSPITALS = []
PEOPLE = []

L = len(HOSPITALS)
ANSWER = 1e9

for x in range(N):
    for y in range(N):
        if MATRIX[x][y] == 2:
            HOSPITALS.append((x, y))
            MATRIX[x][y] = 0
        elif MATRIX[x][y] == 1:
            PEOPLE.append((x, y))

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

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
    res = 0
    for x, y in PEOPLE:
        min_dis = 1e9
        for hx, hy in pairs:
            tmp = abs(hx-x) + abs(hy-y)
            min_dis = tmp if tmp < min_dis else min_dis
        res += min_dis
    ANSWER = res if res < ANSWER else ANSWER
    for x, y in pairs:
        MATRIX[x][y] = 0

print(ANSWER)