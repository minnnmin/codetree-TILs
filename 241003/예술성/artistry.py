from collections import deque

N = int(input())

# 각 좌표의 컬러
COLOR = [list(map(int, input().split())) for _ in range(N)]

# 그룹 정보 (그룹 번호가 쓰여있음. 1이상)
GROUP = [[0 for _ in range(N)] for _ in range(N)]

# 그룹의 (컬러, 멤버 수). 그룹은 1부터니까 0번째는 비워 둠
GROUP_INFO = [()]

# 각 그룹의 대표 좌표. 그룹은 1부터니까 0번째는 비워 둠
GROUP_POS = [()]

# 인접 변 개수 점수. SCORE[i][j]는 그룹 i와 그룹 j의 인접변 개수
SCORE = [[0 for _ in range(30)] for _ in range(30)]

# 초기, 1~3회전 후 예술점수를 여기 쌓아
ANSWER = []

# 인접 변 개수
Q = deque()


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def update_group(x, y, group_num):
    global GROUP, Q, GROUP_INFO, GROUP_POS
    
    Q.append((x, y))
    color = COLOR[x][y]
    GROUP[x][y] = group_num
    GROUP_POS.append((x, y))
    member = 1

    while Q:
        x, y = Q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if in_range(nx, ny) and COLOR[nx][ny] == color and GROUP[nx][ny] == 0:
                GROUP[nx][ny] = group_num
                member += 1
                Q.append((nx, ny))

    GROUP_INFO.append([color, member])


def count_adj_side(x, y, group_num):
    global SCORE
    
    Q.append((x, y))
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[x][y] = True

    while Q:
        x, y = Q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if not in_range(nx, ny) or visited[nx][ny] or GROUP[nx][ny] < group_num: 
                # GROUP[nx][ny] < group_num 라면, 이미 score가 갱신됐을 것이므로 그냥 지나가
                continue
            if GROUP[nx][ny] == group_num:
                visited[nx][ny] = True
                Q.append((nx, ny))
            elif GROUP[nx][ny] > group_num: # 다른 그룹이면 추가 안 하고 점수만 갱신
                SCORE[group_num][GROUP[nx][ny]] += 1
                SCORE[GROUP[nx][ny]][group_num] += 1

# 조화로움 계산
def update_score(g1, g2):
    global SCORE
    # 이때 이미 SCORE에는 그룹 간 인접 변 개수가 저장되어 있음을 유의
    # 점수: (g1 멤버수 + g2 멤버수) * g1 컬러 * g2 컬러 * g1과 g2 인접변 개수
    # 그리고 인접변 개수 0인 애들은 애초에 안 들어옴
    # ANSWER.append((GROUP_INFO[g1][1] + GROUP_INFO[g2][1]) * GROUP_INFO[g1][0] * GROUP_INFO[g2][0] * SCORE[g1][g2])
    return (GROUP_INFO[g1][1] + GROUP_INFO[g2][1]) * GROUP_INFO[g1][0] * GROUP_INFO[g2][0] * SCORE[g1][g2]
    

# 회전 - 십자가
def rotate_cross():
    global COLOR
    # 회전 횟수는 N//2만큼
    for i in range(N//2):
        tmp = COLOR[0+i][N//2]
        COLOR[0+i][N//2] = COLOR[N//2][N-1-i]
        COLOR[N//2][N-1-i] = COLOR[N-1-i][N//2]
        COLOR[N-1-i][N//2] = COLOR[N//2][0+i]
        COLOR[N//2][0+i] = tmp


# 회전 - 나머지 사각형
# 회전할 사각형의 왼쪽상단 꼭짓점 (x, y)와 변의 길이 size를 넣으면 회전시킴
def rotate_square(x, y, size):
    global COLOR

    new = [[0 for _ in range(N)] for _ in range(N)]

    # 위쪽 변 -> 오른쪽 변
    for i in range(size // 2): # size가 5면, 이 안에서 2번 돌아야 됨
        # i는 0, 1
        for j in range(size-1-i, -1+i, -1) : # 겉에서부터 돌아감
            # j는 4, 3, 2, 1, 0 그다음에 3, 2, 1
            new[x+j][y+size-1-i] = COLOR[x+i][y+j]

    # 왼쪽 변 -> 위쪽 변
    for i in range(size // 2): # size가 5면, 이 안에서 2번 돌아야 됨
        # i는 0, 1
        for j in range(size-1-i, -1+i, -1) : # 겉에서부터 돌아감
            # j는 4, 3, 2, 1, 0 그다음에 3, 2, 1
            new[x+i][y+j] = COLOR[x+size-1-j][y+i]

    # 아래 변 -> 왼쪽 변
    for i in range(size // 2): # size가 5면, 이 안에서 2번 돌아야 됨
        # i는 0, 1
        for j in range(i, size-i) : # 겉에서부터 돌아감
            # j는 0, 1, 2, 3, 4 그다음에 1, 2, 3
            new[x+j][y+i] = COLOR[x+size-1-i][y+j]

    # 오른쪽 변 -> 아래 변
    for i in range(size // 2): # size가 5면, 이 안에서 2번 돌아야 됨
        # i는 0, 1
        for j in range(i, size-i) : # 겉에서부터 돌아감
            # j는 0, 1, 2, 3, 4 그다음에 1, 2, 3
            new[x+size-1-i][y+j] = COLOR[x+size-1-j][y+size-1-i]

    # print('뉴 행렬')
    
    for i in range(x, x+size):
        for j in range(y, y+size):
            COLOR[i][j] = new[i][j]

    
for turn in range(4):
    if turn == 4:
        break

    # print(turn, '턴의 color map')
    # for _ in COLOR:
    #     print(_)
    # print()

    # 초기화
    GROUP = [[0 for _ in range(N)] for _ in range(N)]
    GROUP_INFO = [()]
    GROUP_POS = [()]
    SCORE = [[0 for _ in range(30)] for _ in range(30)]

    # 그룹 나누기
    group_num = 1
    for x in range(N):
        for y in range(N):
            if GROUP[x][y] == 0:
                update_group(x, y, group_num)
                group_num += 1
    # print(turn, '턴의 그룹')
    # for _ in GROUP:
    #     print(_)
    # print()
    # 그룹 간 인접 변 개수 세기
    for i, (x, y) in enumerate(GROUP_POS[1:]):
        count_adj_side(x, y, i+1)
    # print(turn, '턴의 GROUP_POS')
    # for _ in GROUP_POS:
    #     print(_)
    # print()
    # 그룹 쌍 지어 조화로움을 계산
    score = 0
    for g1 in range(1, len(GROUP_INFO)):
        for g2 in range(g1, len(GROUP_INFO)):
            if SCORE[g1][g2] != 0:
                score += update_score(g1, g2) # ANSWER 갱신
    ANSWER.append(score)
    # print('ANSWER는', ANSWER)
    rotate_cross()
    rotate_square(0, 0, N//2) # 왼쪽 위
    rotate_square(0, N//2 + 1, N//2) # 오른쪽 위
    rotate_square(N//2 + 1, 0, N//2)
    rotate_square(N//2 + 1, N//2 + 1, N//2)

print(sum(ANSWER))

# for _ in SCORE:
#     print(_)
# print()


# for _ in GROUP:
#     print(_)
# print()

# for _ in GROUP_INFO:
#     print(_)
# print()


# for _ in GROUP:
#     print(_)