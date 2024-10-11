N, M, K = map(int, input().split())

# 벽 정보. 단! 출구가 -1값을 가짐
WALL = [list(map(int, input().split())) for _ in range(N)]

# 참가자 정보: 해당 칸에 참가자 몇명인지
PLAYER = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(M):
    x, y = map(int, input().split())
    PLAYER[x-1][y-1] += 1

x, y = map(int, input().split())
EXIT = (x-1, y-1)
WALL[x-1][y-1] = -1

# 총 이동횟수
ANSWER = 0
# 통과한 사람 수
FINISH = 0
# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def get_dis(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

for sec in range(1, K+1):
    ''' 1. 모든 참가자 동시 이동 '''
    new_player = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if PLAYER[x][y] == 0:
                continue
            now_dis = get_dis((x, y), EXIT)
            num = PLAYER[x][y] # 참가자 수
            min_dis = 1e9 # 출구까지의 거리
            min_d = 4 # 출구까지의 이동방향
            for i in range(4):
                nx, ny = x+dx[i], y+dy[i]
                if not in_range(nx, ny) or WALL[nx][ny] > 0:
                    continue
                dis = get_dis((nx, ny), EXIT)
                if dis >= now_dis:
                    continue
                if dis < min_dis or (dis == min_dis and i < min_d):
                    min_dis = dis
                    min_d = i
            if min_dis == 1e9:
                new_player[x][y] += num
            else:
                nx, ny = x+dx[min_d], y+dy[min_d]
                if (nx, ny) != EXIT:
                    new_player[nx][ny] += num
                else:
                    FINISH += num
                ANSWER += 1*num

    PLAYER = new_player
    # for _ in PLAYER:
    #     print(_)
    # print()
    # for _ in WALL:
    #     print(_)
    # print()
    ''' 모든 참가자가 미로 탈출한 경우 break '''
    # if FINISH == M:
    #     break
    all_finished = True
    for i in range(N):
        for j in range(N):
            if PLAYER[i][j] > 0:
                all_finished = False
                break
    if all_finished:
        break

    ''' 2. 미로 회전 '''
    f_pos = (N, N) # 왼쪽 위 좌표
    f_size = N # 한 변의 길이 -1
    for x in range(N-1):
        for y in range(N-1):
            # (x, y)가 왼쪽 위
            for size in range(1, N):
                # size는 (한 변의 길이 - 1)
                if not in_range(x+size, y+size): # 오른쪽 아래만 범위 검사
                    break
                # 이제 사람1, 출구 포함하는지 확인
                ex, ey = EXIT
                # print(EXIT, 'EXIT')
                if not (x <= ex <= x+size and y <= ey <= y+size):
                    continue
                is_player = False
                for i in range(x, x+size+1):
                    for j in range(y, y+size+1):
                        if PLAYER[i][j] > 0:
                            is_player = True
                            break
                    if is_player:
                        break
                if not is_player:
                    continue
                # 정사각형 조건 통과
                # 이 이후로는 사이즈 더 큰 걸 볼 필요도 없음
                if size < f_size or (size == f_size and x < f_pos[0]) or (size == f_size and x == f_pos[0] and y < f_pos[1]):
                    f_pos = (x, y)
                    f_size = size
                    # break
    # 정사각형이 선택되었음
    # 이제 회전할 차례
    if f_size == N:
        print('문제다.')
    # print('선택된 정사각형', f_pos, f_size+1)
    X, Y = f_pos
    new_wall = [[0 for _ in range(N)] for _ in range(N)]
    new_player = [[0 for _ in range(N)] for _ in range(N)]

    # 사람, 벽 따로 이동. 출구는 WALL에 포함시키자.           
    f_size += 1
    for i in range(f_size):
        for j in range(f_size):
            # print(X+i, Y+j, '를', X+j, f_size-1+Y-i, '로')
            new_wall[X+j][f_size-1+Y-i] = WALL[X+i][Y+j]
            new_player[X+j][f_size-1+Y-i] = PLAYER[X+i][Y+j]

    # 회전 종료
    for x in range(X, X+f_size):
        for y in range(Y, Y+f_size):
            WALL[x][y] = new_wall[x][y]
            if WALL[x][y] > 0:
                WALL[x][y] -= 1
            if WALL[x][y] == -1:
                EXIT = (x, y)
            PLAYER[x][y] = new_player[x][y]
    # for _ in PLAYER:
    #     print(_)
    # print()
    # for _ in WALL:
    #     print(_)
    # print()

print(ANSWER)
print(EXIT[0]+1, EXIT[1]+1)

''' 이거 해바
4 3 8
0 0 0 0
9 2 2 0
0 1 0 1
0 0 0 1
1 1
1 4
4 1
4 3
3 3'''