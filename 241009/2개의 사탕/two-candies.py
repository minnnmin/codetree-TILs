from copy import copy, deepcopy

N, M = map(int, input().split())

MATRIX = []
for _ in range(N):
    MATRIX.append(list(input()))

for i in range(N):
    for j in range(M):
        if MATRIX[i][j] == 'R':
            RED = (i, j)
        elif MATRIX[i][j] == 'B':
            BLUE = (i, j)
        elif MATRIX[i][j] == 'O':
            EXIT = (i, j)

MOVE_LIST = []

DIR = ('UP', 'DOWN', 'RIGHT', 'LEFT')
ANSWER = 1e9

# 백트래킹 (길이 10짜리 수열만들기)
def make_dir_list(n, history):
    global MOVE_LIST

    if n == 11:
        MOVE_LIST.append(history)
        return
    
    for d in DIR:
        if history and d == history[-1]:
            continue
        new_history = copy(history)
        new_history.append(d)
        make_dir_list(n+1, new_history)
        new_history.pop()

# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def play_game(move_list):
    global ANSWER
    # move_list 대로 움직여보고 중간에 성공한 경우 움직인 횟수를 ANSWER에 갱신(Answer보다 작으면)
    # 중간에 파랑 먼저 빠지거나, 같이 빠지거나 하면 그냥 끝
    # 10번 다 돌았는데 안 돼도 끝
    rx, ry = RED
    bx, by = BLUE
    new_matrix = deepcopy(MATRIX)
    # print(move_list)
    for cnt, d in enumerate(move_list):
        if cnt > ANSWER:
            return
        # print('hi2', d)
        if d == 'UP':
            # 만약 빨파의 열이 같으면 행 작은 애 먼저이동
            # 아니면 각자 ++
            # print(rx, ry, bx, by)
            if ry == by:
                if rx < bx: # 빨강 먼저
                    red_finished = False
                    for _ in range(N):
                        nrx, nry = rx+dx[0], ry+dy[0]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            red_finished = True
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            break
                        else:
                            break
                    for _ in range(N):
                        nbx, nby = bx+dx[0], by+dy[0]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O':
                            # print('파랑 통과')
                            return
                        else:
                            break
                    if red_finished:
                        # print('레드만 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        if ANSWER > cnt+1:
                            ANSWER = cnt+1
                        return
                elif rx > bx: # 파랑 먼저
                    for _ in range(N):
                        nbx, nby = bx+dx[0], by+dy[0]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O': # blue먼저 탈출
                            # print('파랑 먼저 통과')
                            return
                        else:
                            break
                    # for _ in new_matrix:
                    #     print(_)
                    for _ in range(N):
                        nrx, nry = rx+dx[0], ry+dy[0]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            if ANSWER > cnt+1:
                                ANSWER = cnt+1
                            return
                        else:
                            break            
            else:
                # 빨강 이동
                red_finished = False
                for _ in range(N):
                    nrx, nry = rx+dx[0], ry+dy[0]
                    if new_matrix[nrx][nry] == '.':
                        new_matrix[rx][ry] = '.'
                        new_matrix[nrx][nry] = 'R'
                        rx, ry = nrx, nry
                    elif new_matrix[nrx][nry] == 'O':
                        red_finished = True
                        new_matrix[rx][ry] = '.'
                        break
                    else:
                        break
                
                # 파랑 이동
                for _ in range(N):
                    nbx, nby = bx+dx[0], by+dy[0]
                    if new_matrix[nbx][nby] == '.':
                        new_matrix[bx][by] = '.'
                        new_matrix[nbx][nby] = 'B'
                        bx, by = nbx, nby
                    elif new_matrix[nbx][nby] == 'O':
                        # print('파랑 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        return
                    else:
                        break
                if red_finished:
                    if ANSWER > cnt+1:
                        ANSWER = cnt+1
                    # print('레드만 통과')
                    # for _ in new_matrix:
                    #     print(_)
                    return
            # print('up 종료')
            # for _ in new_matrix:
            #     print(_)
        elif d == 'DOWN':
            # 만약 빨파의 열이 같으면 행 큰 애 먼저이동
            # 아니면 각자 ++
            if ry == by:
                if rx > bx: # 빨강 먼저
                    red_finished = False
                    for _ in range(N):
                        nrx, nry = rx+dx[1], ry+dy[1]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            red_finished = True
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            break
                        else:
                            break
                    # for _ in new_matrix:
                    #     print(_)
                    for _ in range(N):
                        nbx, nby = bx+dx[1], by+dy[1]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O':
                            # print('파랑 통과')
                            return
                        else:
                            break
                    if red_finished:
                        # print('레드만 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        if ANSWER > cnt+1:
                            ANSWER = cnt+1
                        return
                elif rx < bx: # 파랑 먼저
                    for _ in range(N):
                        nbx, nby = bx+dx[1], by+dy[1]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O': # blue먼저 탈출
                            # print('파랑 먼저 통과')
                            return
                        else:
                            break
                    for _ in range(N):
                        nrx, nry = rx+dx[1], ry+dy[1]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            if ANSWER > cnt+1:
                                ANSWER = cnt+1
                            return
                        else:
                            break            
            else:
                # 빨강 이동
                red_finished = False
                for _ in range(N):
                    nrx, nry = rx+dx[1], ry+dy[1]
                    if new_matrix[nrx][nry] == '.':
                        new_matrix[rx][ry] = '.'
                        new_matrix[nrx][nry] = 'R'
                        rx, ry = nrx, nry
                    elif new_matrix[nrx][nry] == 'O':
                        red_finished = True
                        new_matrix[rx][ry] = '.'
                        break
                    else:
                        break
                
                # 파랑 이동
                for _ in range(N):
                    nbx, nby = bx+dx[1], by+dy[1]
                    if new_matrix[nbx][nby] == '.':
                        new_matrix[bx][by] = '.'
                        new_matrix[nbx][nby] = 'B'
                        bx, by = nbx, nby
                    elif new_matrix[nbx][nby] == 'O':
                        # print('파랑 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        return
                    else:
                        break
                if red_finished:
                    if ANSWER > cnt+1:
                        ANSWER = cnt+1
                    # print('레드만 통과')
                    # for _ in new_matrix:
                    #     print(_)
                    return
            # print('down 후')
            # for _ in new_matrix:
            #     print(_)
        elif d == 'LEFT':
            # 만약 빨파의 행이 같으면 열 작은 애 먼저이동 -> 만약 이때 red가 exit이랑 같아지면 blue도 거기 가는 거라 break
            # 아니면 각자 열--
            if rx == bx:
                if ry < by: # 빨강 먼저
                    red_finished = False
                    for _ in range(M):
                        nrx, nry = rx+dx[2], ry+dy[2]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            red_finished = True
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            break
                        else:
                            break
                    # for _ in new_matrix:
                    #     print(_)
                    for _ in range(M):
                        nbx, nby = bx+dx[2], by+dy[2]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O':
                            # print('파랑 통과')
                            return
                        else:
                            break
                    if red_finished:
                        # print('레드만 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        if ANSWER > cnt+1:
                            ANSWER = cnt+1
                        return
                elif ry > by: # 파랑 먼저
                    # print('파랑 먼저 진행')
                    for _ in range(M):
                        nbx, nby = bx+dx[2], by+dy[2]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O': # blue먼저 탈출
                            # print('파랑 먼저 통과')
                            return
                        else:
                            break
                    for _ in range(M):
                        nrx, nry = rx+dx[2], ry+dy[2]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            if ANSWER > cnt+1:
                                ANSWER = cnt+1
                            return
                        else:
                            break  
                    # print('파랑 다음 빨강 후')
                    # for _ in new_matrix:
                    #     print(_)
            else:
                # 빨강 이동
                red_finished = False
                for _ in range(M):
                    nrx, nry = rx+dx[2], ry+dy[2]
                    if new_matrix[nrx][nry] == '.':
                        new_matrix[rx][ry] = '.'
                        new_matrix[nrx][nry] = 'R'
                        rx, ry = nrx, nry
                    elif new_matrix[nrx][nry] == 'O':
                        red_finished = True
                        new_matrix[rx][ry] = '.'
                        break
                    else:
                        break
                
                # 파랑 이동
                for _ in range(M):
                    nbx, nby = bx+dx[2], by+dy[2]
                    if new_matrix[nbx][nby] == '.':
                        new_matrix[bx][by] = '.'
                        new_matrix[nbx][nby] = 'B'
                        bx, by = nbx, nby
                    elif new_matrix[nbx][nby] == 'O':
                        # print('파랑 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        return
                    else:
                        break
                if red_finished:
                    if ANSWER > cnt+1:
                        ANSWER = cnt+1
                    # print('레드만 통과')
                    # for _ in new_matrix:
                    #     print(_)
                    return
            # print('left 후')
            # for _ in new_matrix:
            #     print(_)
        elif d == 'RIGHT':
            # 만약 빨파의 행이 같으면 열 큰 애 먼저이동 -> 만약 이때 red가 exit이랑 같아지면 blue도 거기 가는 거라 break
            # 아니면 각자 열++
            if rx == bx:
                if ry < by: # 파랑이 오른쪽에 있으면 파랑 먼저
                    for _ in range(M):
                        nbx, nby = bx+dx[3], by+dy[3]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O': # blue먼저 탈출
                            # print('파랑 먼저 통과')
                            return
                        else:
                            break
                    for _ in range(M):
                        nrx, nry = rx+dx[3], ry+dy[3]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            if ANSWER > cnt+1:
                                ANSWER = cnt+1
                            return
                        else:
                            break
                elif ry > by: # 빨강이 오른쪽에 있으면 빨강 먼저
                    red_finished = False
                    for _ in range(M):
                        nrx, nry = rx+dx[3], ry+dy[3]
                        if new_matrix[nrx][nry] == '.':
                            new_matrix[rx][ry] = '.'
                            new_matrix[nrx][nry] = 'R'
                            rx, ry = nrx, nry
                        elif new_matrix[nrx][nry] == 'O':
                            red_finished = True
                            new_matrix[rx][ry] = '.'
                            # print('빨강 통과')
                            break
                        else:
                            break
                    for _ in range(M):
                        nbx, nby = bx+dx[3], by+dy[3]
                        if new_matrix[nbx][nby] == '.':
                            new_matrix[bx][by] = '.'
                            new_matrix[nbx][nby] = 'B'
                            bx, by = nbx, nby
                        elif new_matrix[nbx][nby] == 'O':
                            # print('파랑 통과')
                            return
                        else:
                            break
                    if red_finished:
                        # print('레드만 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        if ANSWER > cnt+1:
                            ANSWER = cnt+1
                        return
            else:
                # 빨강 이동
                red_finished = False
                for _ in range(M):
                    nrx, nry = rx+dx[3], ry+dy[3]
                    if new_matrix[nrx][nry] == '.':
                        new_matrix[rx][ry] = '.'
                        new_matrix[nrx][nry] = 'R'
                        rx, ry = nrx, nry
                    elif new_matrix[nrx][nry] == 'O':
                        red_finished = True
                        new_matrix[rx][ry] = '.'
                        break
                    else:
                        break
                
                # 파랑 이동
                for _ in range(M):
                    nbx, nby = bx+dx[3], by+dy[3]
                    if new_matrix[nbx][nby] == '.':
                        new_matrix[bx][by] = '.'
                        new_matrix[nbx][nby] = 'B'
                        bx, by = nbx, nby
                    elif new_matrix[nbx][nby] == 'O':
                        # print('파랑 통과')
                        # for _ in new_matrix:
                        #     print(_)
                        return
                    else:
                        break
                if red_finished:
                    if ANSWER > cnt+1:
                        ANSWER = cnt+1
                    # print('레드만 통과')
                    # for _ in new_matrix:
                    #     print(_)
                    return
            # print('right 종료')
            # for _ in new_matrix:
            #     print(_)

    # print('아무도 탈출 못함')      
    # for _ in new_matrix:
    #     print(_)


make_dir_list(0, [])
# print(MOVE_LIST)
# MOVE_LIST = [('UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT'), ]
for move_list in MOVE_LIST:
    play_game(move_list)

if ANSWER == 1e9:
    ANSWER = -1

print(ANSWER)