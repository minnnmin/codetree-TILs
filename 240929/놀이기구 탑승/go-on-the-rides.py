N = int(input())

# 학생들의 현위치
STUDENTS = [[0 for _ in range(N)] for _ in range(N)]

LIKE = [[] for _ in range(N*N+1)] # LIKE[3]은 3번 학생이 좋아하는 애들 번호
RIDE_ORDER = [] # 탑승 순서. 학생 번호가 들어있다. 학생 번호는 1이상 N*N 이하

for _ in range(N*N):
    n0, n1, n2, n3, n4 = map(int, input().split())
    RIDE_ORDER.append(n0)
    LIKE[n0] = [n1, n2, n3, n4]

ANSWER = 0 # 점수 총합
like_score = [0, 1, 10, 100, 1000]

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def in_range(x, y):
    return -1 < x < N and -1 < y < N


# student 학생의 위치 정해서 태우기
def ride(student):
    global STUDENTS

    # s_num 학생을 각 자리에 놓을 경우 (인접한 선호학생 수, 인접한 빈칸 수)를 저장
    score = [[0 for _ in range(N)] for _ in range(N)]

    for x in range(N):
        for y in range(N):
            if STUDENTS[x][y] != 0: # 학생이 탑승하고 있으면 pass
                continue
            like, empty = 0, 0
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny):
                    if STUDENTS[nx][ny] == 0:
                        empty += 1
                    elif STUDENTS[nx][ny] in LIKE[student]:
                        like += 1
            score[x][y] = (like, empty)

    like_cnt, empty_cnt = 0, 0
    next_x, next_y = -1, -1
    empty_pos = []
    for x in range(N):
        for y in range(N):
            if STUDENTS[x][y] != 0: # 학생이 탑승하고 있으면 pass
                continue
            like, empty = score[x][y]
            if like > like_cnt or (like == like_cnt and empty > empty_cnt):
                like_cnt, empty_cnt = like, empty
                next_x, next_y = x, y
            elif STUDENTS[x][y] == 0:
                empty_pos.append((x, y))

    # 위에 for문을 돌고 나서 next_x, next_y가 세팅되지 않았을 수 있음
    # 그럴 때는 빈칸이 하나였을 것 
    if (next_x, next_y) == (-1, -1):
        next_x, next_y = empty_pos[0][0], empty_pos[0][1]
        
    STUDENTS[next_x][next_y] = student


def sum_score():
    global ANSWER

    for x in range(N):
        for y in range(N):
            student = STUDENTS[x][y]
            like = 0
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if in_range(nx, ny):
                    if STUDENTS[nx][ny] in LIKE[student]:
                        like += 1
            ANSWER += like_score[like]


for student in RIDE_ORDER:
    ride(student)
sum_score()
print(ANSWER)