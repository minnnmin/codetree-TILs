N, M, K = map(int, input().split())

WALL = [list(map(int, input().split())) for _ in range(N)]
PLAYER = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(M):
    x, y = map(int, input().split())
    PLAYER[x-1][y-1] += 1

x, y = map(int, input().split())
EXIT = [x-1, y-1]
EXIT_MAP = [[0 for _ in range(N)] for _ in range(N)]
EXIT_MAP[x-1][y-1] = 1

# 총 이동횟수
ANSWER = 0

# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N

def move_all_player():
    global ANSWER

    will_move = [] # 이동할 플레이어 정보 (x, y, nx, ny, cnt) cnt는 플레이어 수

    # 이동해야 되는 애들 검사
    for x in range(N):
        for y in range(N):
            player_cnt = PLAYER[x][y]
            if player_cnt != 0:
                now_dis = abs(x - EXIT[0]) + abs(y - EXIT[1])
                new_dis = now_dis
                new_x, new_y = -1, -1
                for i in range(4): # 상하좌우 순으로 검사
                    nx, ny = x+dx[i], y+dy[i]
                    if in_range(nx, ny) and WALL[nx][ny] == 0 and (new_dis > (abs(nx - EXIT[0]) + abs(ny - EXIT[1]))):
                        new_dis = abs(nx - EXIT[0]) + abs(ny - EXIT[1])
                        new_x, new_y = nx, ny
                if (new_x, new_y) != (-1, -1):
                    will_move.append((x, y, new_x, new_y, player_cnt))
    
    # 실제 이동
    if will_move:
        for x, y, nx, ny, cnt in will_move:
            if (nx, ny) == (EXIT[0], EXIT[1]): # 출구 도착
                PLAYER[x][y] = 0
            else:
                # print('왜 안돼', x, y, nx, ny, cnt)
                PLAYER[nx][ny] += cnt
                PLAYER[x][y] -= cnt
            ANSWER += (abs(x-nx) + abs(y-ny))*cnt


# EXIT와 함께 꼭짓점이 될 좌표 (x, y)와 대각선 관계(1)인지 아닌지(0)
# dis는 꼭짓점~출구 거리
def get_4_vertex(vertex_x, vertex_y, diagonal, dis):
    # print(vertex_x, vertex_y, diagonal, dis)
    if diagonal:
        if vertex_x < EXIT[0] and vertex_y < EXIT[1]:
            left_up, right_up, left_down, right_down = \
                (vertex_x, vertex_y), (vertex_x, vertex_y+dis), (vertex_x+dis, vertex_y), (EXIT[0], EXIT[1])
        elif vertex_x < EXIT[0] and vertex_y > EXIT[1]:
            left_up, right_up, left_down, right_down = \
                (vertex_x, vertex_y-dis), (vertex_x, vertex_y), (EXIT[0], EXIT[1]), (vertex_x+dis, vertex_y)
        elif vertex_x > EXIT[0] and vertex_y < EXIT[1]:
            left_up, right_up, left_down, right_down = \
                (vertex_x-1, vertex_y), (EXIT[0], EXIT[1]), (vertex_x, vertex_y), (vertex_x, vertex_y+1)
        elif vertex_x > EXIT[0] and vertex_y > EXIT[1]:
            left_up, right_up, left_down, right_down = \
                (EXIT[0], EXIT[1]), (vertex_x-1, vertex_y), (vertex_x, vertex_y-1), (vertex_x, vertex_y)
    
    else: # 이게 무조건 꼭짓점이 되는 건 아님
        if vertex_x < EXIT[0]: # V가 E 위에 있을 경우
            if dis > vertex_y:
                left_up, right_up, left_down, right_down = \
                    (vertex_x, 0), (vertex_x, dis), (EXIT[0], 0), (EXIT[0], dis)
            elif dis <= vertex_y:
                left_up, right_up, left_down, right_down = \
                    (vertex_x, vertex_y-dis), (vertex_x, vertex_y), (EXIT[0], EXIT[1]-dis), (EXIT[0], EXIT[1])
        elif vertex_x > EXIT[0]: # V가 E 아래 있을 경우
            if dis > vertex_y:
                left_up, right_up, left_down, right_down = \
                    (EXIT[0], 0), (EXIT[0], dis), (vertex_x, 0), (vertex_x, dis)
            elif dis <= vertex_y:
                left_up, right_up, left_down, right_down = \
                    (EXIT[0], EXIT[1]-dis), (EXIT[0], EXIT[1]), (vertex_x, vertex_y-dis), (vertex_x, vertex_y)
        elif vertex_y < EXIT[1]: # V가 E 왼쪽에 있을 경우
            if dis > vertex_x:
                left_up, right_up, left_down, right_down = \
                    (0, vertex_y), (0, EXIT[1]), (dis, vertex_y), (dis, EXIT[1])
            elif dis <= vertex_x:
                left_up, right_up, left_down, right_down = \
                    (vertex_x-dis, vertex_y), (EXIT[0]-dis, EXIT[1]), (vertex_x, vertex_y), (EXIT[0], EXIT[1])
        elif vertex_y > EXIT[1]: # V가 E 오른쪽에 있을 경우
            if dis > vertex_x:
                # print('이거 아니니?')
                # print('EXIT', EXIT)
                left_up, right_up, left_down, right_down = \
                    (0, EXIT[1]), (0, vertex_y), (dis, EXIT[1]), (dis, vertex_y)
            elif dis <= vertex_x:
                left_up, right_up, left_down, right_down = \
                    (EXIT[0]-dis, EXIT[1]), (vertex_x-dis, vertex_y), (EXIT[0], EXIT[1]), (vertex_x, vertex_y)

    return left_up, right_up, left_down, right_down

# 참가자 없으면 돌지 마라
def get_min_square():

    min_dis = 19
    min_dis_players = [] # min_dis 거리에 있는 플레이어들 좌표 (x, y)
    diagonal = [] # 대각선 관계에 있는 애들
    not_diagonal = [] # 대각선 관계가 아닌, 수직이나 수평 관계에 애들

    # 출구, 참가자 최소 1명 포함하는 사각형 찾기
    for dis in range(1, 19): # 최대 거리 18임 (NxN 좌상단 우하단 거리 18)
        for x in range(-dis, dis+1):
            for y in range(-dis, dis+1):
                nx, ny = EXIT[0] + x, EXIT[1] + y
                if in_range(nx, ny) and abs(x-y) == dis:
                    if PLAYER[nx][ny] > 0: # 이 위치를 포함시키면 됨
                        if nx == EXIT[0] or ny == EXIT[1]:
                            not_diagonal.append((nx, ny))
                        else:
                            diagonal.append((nx, ny))
        if diagonal or not_diagonal:
            min_dis = dis
            break

    # 어떤 걸로 정사각형 만들어야 r, c가 최소가 될까
    if diagonal:
        vertex_x, vertex_y = diagonal[0][0], diagonal[0][1]
        for x, y in diagonal[1:]:
            if x < vertex_x or (x == vertex_x and y < vertex_y):
                vertex_x, vertex_y = x, y
    elif not_diagonal:
        vertex_x, vertex_y = not_diagonal[0][0], not_diagonal[0][1]
        for x, y in not_diagonal[1:]:
            if x < vertex_x or (x == vertex_x and y < vertex_y):
                vertex_x, vertex_y = x, y
    else:
        print('돌 수 없음. 이게 출력되면 안 된다. 그전에 제어할 것')
        # for _ in PLAYER:
        #     print(_)
    
    return vertex_x, vertex_y, 1 if diagonal else 0, min_dis
    # 자 이제 vertex4 가 4개의 꼭짓점이다
    

# 꼭짓점 4개를 넣어주면 참가자, 벽, EXIT 돌려버림 # 순서대로 좌상, 우상, 좌하, 우하
def rotate(left_up, right_up, left_down, right_down):
    global PLAYER, WALL

    dis = right_up[1] - left_up[1]
    tmp_up_player = PLAYER[left_up[0]][left_up[1]:right_up[1]+1]
    tmp_up_wall = WALL[left_up[0]][left_up[1]:right_up[1]+1]
    tmp_up_exit = EXIT_MAP[left_up[0]][left_up[1]:right_up[1]+1]

    # 좌측 애들 위측으로 싹 이동 한칸
    left_player = []
    left_wall = []
    left_exit = []
    for i in range(dis+1):
        left_player.append(PLAYER[left_down[0] - i][left_up[1]])
        if WALL[left_down[0] - i][left_up[1]] > 0:
            left_wall.append(WALL[left_down[0] - i][left_up[1]]-1)
        else:
            left_wall.append(WALL[left_down[0] - i][left_up[1]])
        left_exit.append(EXIT_MAP[left_down[0] - i][left_up[1]])
    i = 0
    for j in range(left_up[1], right_up[1]+1):
        PLAYER[left_up[0]][j] = left_player[i]
        WALL[left_up[0]][j] = left_wall[i]
        EXIT_MAP[left_up[0]][j] = left_exit[i]
        i += 1
    

    # 아래 애들 왼쪽으로 싹 이동 한칸
    down_player = PLAYER[left_down[0]][left_down[1]:right_down[1]+1]
    down_wall = WALL[left_down[0]][left_down[1]:right_down[1]+1]
    down_exit = EXIT_MAP[left_down[0]][left_down[1]:right_down[1]+1]
    i = 0
    for x in range(left_up[0], left_down[0]+1):
        PLAYER[x][left_up[1]] = down_player[i]
        if down_wall[i] > 0:
            WALL[x][left_up[1]] = down_wall[i] - 1
        else:
            WALL[x][left_up[1]] = down_wall[i]
        EXIT_MAP[x][left_up[1]] = down_exit[i]
        i += 1
    

    # 우측 애들 아래로 싹 이동 한칸
    right_player = []
    right_wall = []
    right_exit = []
    for x in range(right_down[0], right_up[0]-1, -1):
        right_player.append(PLAYER[x][right_up[1]])
        right_wall.append(WALL[x][right_up[1]])
        right_exit.append(EXIT_MAP[x][right_up[1]])
    right_player[-1] = tmp_up_player[-1]
    right_wall[-1] = tmp_up_wall[-1]
    right_exit[-1] = tmp_up_exit[-1]
    i = 0
    for y in range(left_down[1], right_down[1]+1):
        PLAYER[left_down[0]][y] = right_player[i]
        if right_wall[i] > 0:
            WALL[left_down[0]][y] = right_wall[i] - 1
        else:
            WALL[left_down[0]][y] = right_wall[i]
        EXIT_MAP[left_down[0]][y] = right_exit[i]
        i += 1
    
    # 위쪽 애들 오른쪽으로 싹 이동 한칸
    tmp_up_player.reverse()
    tmp_up_wall.reverse()
    tmp_up_exit.reverse()
    i = 0
    for x in range(right_down[0], right_up[0]-1, -1):
        print(tmp_up_player, i)
        PLAYER[x][right_down[1]] = tmp_up_player[i]
        if tmp_up_wall[i] > 0:
            WALL[x][right_down[1]] = tmp_up_wall[i] - 1
        else:
            WALL[x][right_down[1]] = tmp_up_wall[i]
        EXIT_MAP[x][right_down[1]] = tmp_up_exit[i]
        i += 1


for k in range(K):
    # 플레이어 없으면 없애야 함
    there_is_player = False
    # for rows in PLAYER:
    #     if sum(rows) > 0:
    #         there_is_player = True
    #         break
    # if not there_is_player:
    #     break
    # print('전')
    # for _ in PLAYER:
    #     print(_)
    # print()
    PLAYER[EXIT[0]][EXIT[1]] = 0 
    move_all_player()
    # print('1. 이동 후')
    # for _ in PLAYER:
    #     print(_)
    # print()
    there_is_player = False
    for rows in PLAYER:
        if sum(rows) > 0:
            there_is_player = True
            break
    if not there_is_player:
        break
    # for _ in WALL:
    #     print(_)
    # print()
    vertex_x, vertex_y, diagonal, dis = get_min_square()
    left_up, right_up, left_down, right_down = get_4_vertex(vertex_x, vertex_y, diagonal, dis)
    
    # print('2. 네 꼭짓점을 정한 후')
    # print(left_up, right_up, left_down, right_down)

    # 젤 겉에 사각형부터 넣어줌
    if dis % 2 == 0:
        for i in range((dis+2)//2): # d=4; 3회; 마지막 1회는 안 해도 됨
            left_up = (left_up[0]+1*i, left_up[1]+1*i)
            right_up = (right_up[0]+1*i, right_up[1]-1*i)
            left_down = (left_down[0]-1*i, left_down[1]+1*i)
            right_down = (right_down[0]-1*i, right_down[1]-1*i)
            if left_up == left_down == right_up == right_down:
                if WALL[left_up[0]][left_up[1]] > 0:
                    WALL[left_up[0]][left_up[1]] -= 1
                break
            rotate(left_up, right_up, left_down, right_down)
    else:
        for i in range((dis+2)//2):
            left_up = (left_up[0]+1*i, left_up[1]+1*i)
            right_up = (right_up[0]+1*i, right_up[1]-1*i)
            left_down = (left_down[0]-1*i, left_down[1]+1*i)
            right_down = (right_down[0]-1*i, right_down[1]-1*i)
            rotate(left_up, right_up, left_down, right_down)
    
    # print('2. 회전 후')
    for r in range(N):
        for c in range(N):
            if EXIT_MAP[r][c] == 1:
                EXIT = [r, c]
    # print('출구', EXIT)
    # for _ in WALL:
    #     print(_)
    # print()

    # print('후')
    # for _ in PLAYER:
    #     print(_)
    # print()
    # for _ in WALL:
    #     print(_)

print(ANSWER)
EXIT[0] += 1
EXIT[1] += 1
print(*EXIT)