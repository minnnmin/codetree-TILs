from copy import deepcopy

N = int(input())
PEOPLE = [list(map(int, input().split())) for _ in range(N)]

# 이동거리 쌍: [(이동거리1, 이동거리2), ] 
DIS_PAIR = []
# 가능한 직사각형의 정보: [(시작점 좌표), 이동거리1, 이동거리2]
RECTANGLE = []

# 동, 북, 서, 남 (대각선)
dx = [-1, -1, 1, 1]
dy = [1, -1, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

# 부족별 인구수 abs(최대값-최소값) - 최소가 되어야 함
ANSWER = 1e9


def get_people(start, dis1, dis2):
    global ANSWER

    group = [[0 for _ in range(N)] for _ in range(N)]

    X1, Y1 = start
    X2, Y2 = X1+dx[0]*dis1, Y1+dy[0]*dis1
    X3, Y3 = X2+dx[1]*dis2, Y2+dy[1]*dis2
    X4, Y4 = X3+dx[2]*dis1, Y3+dy[2]*dis1

    # 1번 경계 세팅
    x, y = start
    group[x][y] = 1
    for _ in range(dis1):
        x, y = x+dx[0], y+dy[0]
        group[x][y] = 1
    for _ in range(dis2):
        x, y = x+dx[1], y+dy[1]
        group[x][y] = 1
    for _ in range(dis1):
        x, y = x+dx[2], y+dy[2]
        group[x][y] = 1
    for _ in range(dis2):
        x, y = x+dx[3], y+dy[3]
        group[x][y] = 1
    
    # 2번 세팅
    for i in range(X4):
        for j in range(Y3+1):
            if group[i][j] == 0:
                group[i][j] = 2
            elif group[i][j] == 1:
                break

    # 4번 세팅
    for i in range(X4, N):
        for j in range(Y1):
            if group[i][j] == 0:
                group[i][j] = 4
            elif group[i][j] == 1:
                break

    # 3번 세팅
    for i in range(X2+1):
        for j in range(N-1, 0, -1):
            if group[i][j] == 0:
                group[i][j] = 3
            elif group[i][j] != 0:
                break

    # 5번 세팅
    for i in range(X2+1, N):
        for j in range(N-1, 0, -1):
            if group[i][j] == 0:
                group[i][j] = 5
            elif group[i][j] != 0:
                break

    # 1번 내부 세팅
    for i in range(N):
        for j in range(N):
            if group[i][j] == 0:
                group[i][j] = 1

    people_cnt = [0, 0, 0, 0, 0, 0] # 1~5 순서대로 # 맨앞 안씀. 그냥 1번이랑 같은 번호 해.
    for i in range(N):
        for j in range(N):
            if group[i][j] == 1:
                people_cnt[0] += PEOPLE[i][j]
                people_cnt[1] += PEOPLE[i][j]
            elif group[i][j] == 2:
                people_cnt[2] += PEOPLE[i][j]
            elif group[i][j] == 3:
                people_cnt[3] += PEOPLE[i][j]
            elif group[i][j] == 4:
                people_cnt[4] += PEOPLE[i][j]
            elif group[i][j] == 5:
                people_cnt[5] += PEOPLE[i][j]

    dis = max(people_cnt) - min(people_cnt)
    if dis < ANSWER:
        ANSWER = dis

''' 1. 직사각형 정의 '''
# 이동거리 쌍 만들기
for dis1 in range(1, N-1):
    for dis2 in range(1, N-1):
        DIS_PAIR.append((dis1, dis2))

# 시작점이 될 좌표
for x in range(2, N):
    for y in range(1, N-1):
        for dis1, dis2 in DIS_PAIR:
            x2, y2 = x+dx[0]*dis1, y+dy[0]*dis1
            x3, y3 = x2+dx[1]*dis2, y2+dy[1]*dis2
            x4, y4 = x3+dx[2]*dis1, y3+dy[2]*dis1
            if in_range(x2, y2) and in_range(x3, y3) and in_range(x4, y4):
                RECTANGLE.append(((x, y), dis1, dis2))

# for _ in RECTANGLE:
#     print(_)
''' 2. 부족별 인구수 계산 '''
for (x, y), dis1, dis2 in RECTANGLE:
    get_people((x, y), dis1, dis2)


# (x, y), dis1, dis2 = RECTANGLE[-4]
# print(x, y, dis1, dis2)
# get_people((x, y), dis1, dis2)

print(ANSWER)