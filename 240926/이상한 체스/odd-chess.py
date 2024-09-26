N, M = map(int, input().split())
CHESS = [list(map(int, input().split())) for _ in range(N)]
MY_CHESSMEN = [] 
for i in range(N):
    for j in range(M):
        if 0 < CHESS[i][j] < 6:
            MY_CHESSMEN.append([i, j, CHESS[i][j]])
MY_CHESSMEN.append([]) # 마지막 재귀실행을 위해

# MY_CHESSMEN : [[1, 1, 2], [2, 3, 5], [3, 1, 1], []] => [x, y, 말 번호]

MIN_CANT_GO = 64

# 체스말 별 이동 가능한 방향 셋 (0번 말 없으므로 비워두고)
# 예를 들어 2번 말의 경우 [위, 아래], [좌, 우] 이런 세트로 이동 가능함
CAN_GO_DIR = [[],
              [0, 1, 2, 3],
              [[0, 2], [1, 3]],
              [[0, 1], [1, 2], [2, 3], [3, 0]],
              [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]],
              [[0, 1, 2, 3]]]


# CHESS 판의 0 개수를 세서 리턴
def count_zero():
    tmp = 0
    for i in range(N):
        for j in range(M):
            if CHESS[i][j] == 0:
                tmp += 1

    return tmp
    

# id: 0, 1, 2, 3은 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


# 7은 이동 가능한 곳이라는 표시
# 해당 방향으로 갈 수 있는 만큼 가면서, 0에서 7로 바꾼 곳의 위치를 리스트로 리턴
# (x, y)에서 d방향으로 갈 수 있는 만큼 가보기
def move(x, y, d):
    global CHESS
    
    add_7_pos = []

    nx = x
    ny = y

    for i in range(8):
        nx += dx[d]
        ny += dy[d]
        if -1 < nx < N and -1 < ny < M and CHESS[nx][ny] != 6:
            # 갈 수 있다
            if CHESS[nx][ny] == 0:
                add_7_pos.append([nx, ny])
                CHESS[nx][ny] = 7
        else:
            # 못 가면 끝내
            break

    return add_7_pos


# 백트래킹 함수
# n은 지금이 몇 번째 턴인지 -> MY_CHESSMEN 순서와 동일
# my_chessmen은 [x, y, 말 번호]
def main(n, my_chessmen):
    global MIN_CANT_GO

    if n == len(MY_CHESSMEN) - 1:
        res = count_zero()
        MIN_CANT_GO = res if res < MIN_CANT_GO else MIN_CANT_GO
        return
    
    now_x = my_chessmen[0]
    now_y = my_chessmen[1]
    now_chessmen_num = my_chessmen[2]

    # 이번 턴에 검사할 말의 모든 방향을 탐색
    # 방향 하나 선택 후, 그 방향으로 이동하면서 0이었던 곳만 7로 변경
    # 자신이 7로 바꾼 곳의 위치를 저장해두고, 함수 종료 후 원복
    for dirs in CAN_GO_DIR[now_chessmen_num]:
        add_7_pos = [] # 여기에 7로 변경한 곳의 좌표를 더해
        if now_chessmen_num == 1:
            add_7_pos += move(now_x, now_y, dirs)
            main(n+1, MY_CHESSMEN[n+1])
            if add_7_pos:
                for x, y in add_7_pos:
                    CHESS[x][y] = 0
                add_7_pos.clear()
        else: # 검사할 방향이 2개 이상인 경우
            for d in dirs:
                add_7_pos += move(now_x, now_y, d)
            main(n+1, MY_CHESSMEN[n+1])
            if add_7_pos:
                for x, y in add_7_pos:
                    CHESS[x][y] = 0
                add_7_pos.clear()



# 그럼 main 호출 시 n을 1부터 시작해야 하나
main(0, MY_CHESSMEN[0])
print(MIN_CANT_GO)