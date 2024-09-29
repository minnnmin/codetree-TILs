from copy import deepcopy


N = int(input())
PEOPLE = [list(map(int, input().split())) for _ in range(N)]


# 완성된 직사각형의 좌표 모음
RECTANGLE = []


# 인구 차이 최소값
PEOPLE_DIFF = 1e9


# 동, 북, 서, 남 (대각선)
dx = [-1, -1, 1, 1]
dy = [1, -1, -1, 1]


# 현재 위치, 현재 위치로 올 때의 방향, 지나온 좌표 모음
def dfs(x, y, d, history):
    # if d > 3:
    #     return
    if d == 3 and (x, y) == (history[0][0], history[0][1]):
        # 기울어진 직사각형 완성
        # print('x, y, d, history', x, y, d, history)
        history.pop()
        RECTANGLE.append(history)
        return
    if d == 3 and x >= history[0][0]:
        return
    if not (-1 < x < N and -1 < y < N):
        return


    # 현재 방향 유지
    new_history1 = deepcopy(history)
    new_history1.append((x+dx[d], y+dy[d]))
    dfs(x+dx[d], y+dy[d], d, new_history1)
    
    # 다음 방향으로 변경
    if d < 3:
        new_history2 = deepcopy(history)
        new_history2.append((x+dx[(d+1)%4], y+dy[(d+1)%4]))
        dfs(x+dx[(d+1)%4], y+dy[(d+1)%4], (d+1)%4, new_history2)


# 기울어진 직사각형들의 좌표를 넣어주고, 1~5 부족의 인구수를 센 다음, 최대-최소 값을 전역변수 PEOPLE_DIFF에 갱신
def count_people(rectangle):
    global PEOPLE_DIFF

    # 4개의 꼭지점 추출
    up, down, left, right = rectangle[0], rectangle[0], rectangle[0], rectangle[0]
    for x, y in rectangle:
        if x < up[0]:
            up = (x, y)
        if x > down[0]:
            down = (x, y)
        if y < left[1]:
            left = (x, y)
        if y > right[1]:
            right = (x, y)
    
    # 그룹 번호 (0은 할당 전. 끝났는데 0있으면 안됨)
    group = [[0 for _ in range(N)] for _ in range(N)]
    # 사각형 변부터 그룹에 표시
    for x, y in rectangle:
        group[x][y] = 1
    # for _ in group:
    #     print(_)
    # print()
    # 1 안쪽 1표시
    for i in range(up[0], down[0]+1):
        one_pos = []
        for j in range(left[1], right[1]+1):
            if group[i][j] == 1:
                one_pos.append((i, j))
        if len(one_pos) == 2:
            l, r = one_pos[0], one_pos[1]
            for x in range(l[1], r[1]):
                group[i][x] = 1

    # 1은 그냥 좌표값의 합 + 그 가운데 있는 애들은 제일 마지막에 체크할까?
    # 2의 x는 0~왼꼭x-1, y는 0~위꼭y까지
    for x in range(0, left[0]):
        for y in range(0, up[1]+1):
            if group[x][y] == 0:
                group[x][y] = 2

    # 3의 x는 0부터 오른쪽꼭지 x까지, y는 위꼭 y+1~ N-1까지
    for x in range(0, right[0]+1):
        for y in range(up[1], N):
            if group[x][y] == 0:
                group[x][y] = 3

    # 4의 x는 왼꼭x부터 N-1, y는 0~아래꼭y-1
    for x in range(left[0], N):
        for y in range(0, down[1]):
            if group[x][y] == 0:
                group[x][y] = 4

    # 5의 x는 오꼭 x+1부터 N-1, y는 아래꼭y~n
    for x in range(right[0]+1, N):
        for y in range(down[1], N):
            if group[x][y] == 0:
                group[x][y] = 5
    
    # 마지막으로 1 내부 표시
    for x in range(up[0]+1, down[0]):
        for y in range(left[0]+1, right[1]):
            if group[x][y] == 0:
                group[x][y] = 1
    
    # for _ in group:
    #     print(_)

    group_people = [0 for _ in range(N+1)]

    for i in range(N):
        for j in range(N):
            gid = group[i][j]
            group_people[gid] += PEOPLE[i][j]

    # print(group_people)
    tmp_min_cnt = 1e9
    for cnt in group_people:
        if 0 < cnt < tmp_min_cnt:
            tmp_min_cnt = cnt

    res = max(group_people) - tmp_min_cnt
    # print(group_people)
    if res < PEOPLE_DIFF:
        PEOPLE_DIFF = res


# for문 돌려서 기울어진 직사각형 만들어보기 - 이거 끝나면 RECTANGLE 세팅
for i in range(2, N):
    for j in range(1, N-1):
        nx, ny = i+dx[0], j+dy[0]
        dfs(nx, ny, 0, [(i, j), (nx, ny)])

for rec in RECTANGLE:
    count_people(rec)

print(PEOPLE_DIFF)


# tmp_rec = [(1, 3), (2, 2), (2, 4), (3, 1), (3, 5), (4, 2), (4, 4), (5, 3)]
# count_people(tmp_rec)

# [[0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 1, 0, 1, 0, 0],
#  [0, 1, 0, 0, 0, 1, 0],
#  [0, 0, 1, 0, 1, 0, 0],
#  [0, 0, 0, 1, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0]]

# count_people(RECTANGLE)


# for i in range(len(RECTANGLE)):
#     # print(RECTANGLE[i]) # [(2, 1), (1, 2), (0, 1), (1, 0), (2, 1)]
#     tmp = [[0 for _ in range(N)] for _ in range(N)]
#     for x, y in RECTANGLE[i]:
#         tmp[x][y] = 1
#     for _ in tmp:
#         print(_)
#     print()


# for rec in RECTANGLE:
#     count_people(rec)

# print(PEOPLE_DIFF)