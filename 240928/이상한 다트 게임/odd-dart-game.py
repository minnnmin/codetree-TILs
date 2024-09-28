from collections import deque

# 원판의 개수 N, 원판 내의 숫자의 개수 M, 회전 횟수 Q
N, M, Q = map(int, input().split())

# 다트판 정보
DARTS = [list(map(int, input().split())) for _ in range(N)]


# 회전 명령
ROTATE_ORDER = []
for q in range(Q):
    x, d, k = map(int, input().split())
    ROTATE_ORDER.append((x-1, d, k))
    # 회전하는 원판의 종류 x, 방향 d, 회전하는 칸 수 k


# print('전')
# for _ in DARTS:
#     print(_)


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def rotate(dart_num, rotate_dir, rotate_cnt):
    # 만약 회전 방향이 숫자 개수의 배수면 돌리지마
    if rotate_cnt % M == 0:
        return
    
    # 돌려야 되는 얘의 배수만 돌려야 됨
    if rotate_dir == 0: # 시계 방향
        for i in range(dart_num, len(DARTS), dart_num+1):
            DARTS[i] = DARTS[i][M-rotate_cnt:] + DARTS[i][:M-rotate_cnt]
    else: # 반시계 방향
        for i in range(dart_num, len(DARTS), dart_num+1):
            DARTS[i] = DARTS[i][rotate_cnt:] + DARTS[i][:rotate_cnt]



def in_range(x, y):
    return -1 < x < N and -1 < y < M


q = deque()
del_group = [] # 인접한 같은 수들의 좌표


def bfs(start): # 시작점 좌표 (x, y)
    
    visited = [[False for _ in range(M)] for _ in range(N)]

    q.append(start)
    del_group.append(start)

    visited[start[0]][start[1]] = True
    num = DARTS[start[0]][start[1]]

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if in_range(nx, ny) and not visited[nx][ny] and DARTS[nx][ny] == num:
                q.append((nx, ny))
                visited[nx][ny] = True
                del_group.append((nx, ny))


def get_darts_avg():
    cnt = 0
    sum_of_nums = 0

    for i in range(N):
        for j in range(M):
            if DARTS[i][j] != 0:
                cnt += 1
                sum_of_nums += DARTS[i][j]

    return sum_of_nums//cnt


def normalization():
    avg = get_darts_avg()

    for i in range(N):
        for j in range(M):
            if DARTS[i][j] == 0:
                continue
            if DARTS[i][j] > avg:
                DARTS[i][j] -= 1
            elif DARTS[i][j] < avg:
                DARTS[i][j] += 1

# 원판에 남은 수가 있는지 확인
def num_in_darts():
    for i in range(N):
        for j in range(M):
            if DARTS[i][j] != 0:
                return True
    return False


# 회전하는 원판의 종류 x, 방향 d, 회전하는 칸 수 k
for x, d, k in ROTATE_ORDER:
    rotate(x, d, k)
    for i in range(N):
        for j in range(M):
            if DARTS[i][j] != 0:
                del_group = []
                bfs((i, j))
                # print('후')
                # for _ in DARTS:
                #     print(_)
                # print('del_group', del_group)
                if len(del_group) > 1:
                    # 인접 숫자 삭제
                    for nx, ny in del_group:
                        DARTS[nx][ny] = 0
                else:
                    # 원판에 남은 수가 있으면 정규화
                    if not num_in_darts():
                        normalization()

answer = 0
for i in range(N):
    for j in range(M):
        answer += DARTS[i][j]

print(answer)