N, M, H = map(int, input().split())
R, C = H+2, N*2-1

LOSS_LINES_STATE = [[0 for _ in range(C)] for _ in range(R)]
PLAYERS_POS = [(R-1, i*2) for i in range(N)] # 0~N-1번째 플레이어들의 초기 위치

for _ in range(M):
    x, y = map(int, input().split())
    LOSS_LINES_POS.append((x, y*2-1))
    LOSS_LINES_STATE[x][y*2-1] = 1 # 초기 유실선 배치

def in_range(x, y):
    return -1 < x < R and -1 < y < C

# 데이터 이동 - 이 함수 실행 후, 각 플레이어가 자신의 열은 유지한 채 행만 0으로 바뀌었다면 성공인
# 이 함수는 그냥 현재 맵에 따라서 이동하는 것
def move_data():
    # 최종위치
    final_pos = []
    # 한명씩 꺼내서 맵에 따라 이동시켜보고, 만약 최종도달지의 열이 자신의 열과 달라지면 break. 불가능
    for pid, (x, y) in enumerate(PLAYERS_POS): # pid는 플레이어 번호(0~N-1)
        # 해당 플레이어를 끝까지 이동시켜보기
        nx, ny = x, y
        while nx != 0:
            nx -= 1
            # 좌측 검사
            if in_range(nx, ny-1) and LOSS_LINES_STATE[nx][ny-1] == 1:
                ny -= 2
            # 우측
            elif in_range(nx, ny+1) and LOSS_LINES_STATE[nx][ny+1] == 1:
                ny += 2
        if ny != y:
            return False
    return True
    # return False

AVAILABLE = False
# n은 현재 놓아진 유실선 개수. 최초 호출 시 0이어야겠지
def backtracking(n):
    global LOSS_LINES_STATE, AVAILABLE

    if n == ANSWER:
        if move_data(): # 만약 이동했는데 된다면 전역변수 AVAILABLE를 True로 갱신
            AVAILABLE = True
        return
    
    for x in range(R-1):
        for y in range(1, C-1, 2):
            # 좌우에 유실선 없으면 (x, y)에 유실선 놓아보기
            if LOSS_LINES_STATE[x][y]:
                continue
            if (not in_range(x, y-2) or LOSS_LINES_STATE[x][y-2] == 0)\
                and (not in_range(x, y+2) or LOSS_LINES_STATE[x][y+2] == 0):
                LOSS_LINES_STATE[x][y] = 1
                backtracking(n+1)
                LOSS_LINES_STATE[x][y] = 0


# 현재까지 새로 추가한 메모리 유실선 개수
ANSWER = 0
for i in range(4):
    if ANSWER >= 3:
        ANSWER = -1
    if move_data():
        break
    else:
        ANSWER += 1
        AVAILABLE = False
        backtracking(0)
        if AVAILABLE:
            # print(ANSWER, '개 놓고 성공해서 끝남')
            break
        # 유실선 개수를 1개 추가한 다음, 백트래킹 돌면서 유실선 놓아보기
        # 만약 유실선을 ANSWER만큼 더 놓을 수 없다면 불가능한 거니까 break
        # 만약 백트래킹 돌고 나서 AVAILABLE이 True면? 그때 끝내

print(ANSWER)