N, M = map(int, input().split())
car_x, car_y, car_d = map(int, input().split())

matrix = []

for _ in range(N):
    matrix.append(list(map(int, input().split())))

visited = [[False for _ in range(M)] for _ in range(N)]
visited[car_x][car_y] = True

# 상, 우, 하, 좌: 0, 1, 2, 3
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def cango(x, y): #x, y로 이동 가능?
    if -1 < x < N and -1 < y < M and not visited[x][y] and matrix[x][y] == 0:
        return True
    return False


def move_left():
    global car_x, car_y, car_d
    # 4방향 모두 확인
    new_d = car_d
    for i in range(4):
        new_d = (new_d + 3)%4
        new_x = car_x + dx[new_d]
        new_y = car_y + dy[new_d]
        if cango(new_x, new_y):
            visited[new_x][new_y] = True
            car_x, car_y, car_d = new_x, new_y, new_d
            return True
    # if car_d 가 0이면 3을 1이면0을 2면1을 3이면2를 (+3을 4로 나눈 나머지)
    #     pass
    return False # 4방향 모두 전진하지 못한 경우

def move_back():
    global car_x, car_y
    # 방향 유지한 채로 후진 # 0이면2로  1이면3으로  2면0으로  3이면1로
    tmp_d = (car_d+2)%4
    tmp_x = car_x + dx[tmp_d]
    tmp_y = car_y + dy[tmp_d]
    if -1 < tmp_x < N and -1 < tmp_y < M and matrix[tmp_x][tmp_y] == 0:
        car_x, car_y = tmp_x, tmp_y
        return True
    # 불가능한 경우
    else:
        return False

# 후진을 못하면 break
while True:
    if move_left():
        continue
    else:
        result = move_back()
        if not result:
            break

answer = 0
for v in visited:
    answer += v.count(1)

print(answer)