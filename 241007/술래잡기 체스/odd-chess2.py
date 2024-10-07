# 도둑 현 위치
MATRIX = []
THIEVES_INFO = {} # 도둑 번호: (x, y, d), 죽은 도둑: 'DEAD'

for _ in range(4):
    t1, d1, t2, d2, t3, d3, t4, d4 = map(int, input().split())
    MATRIX.append([(t1, d1-1), (t2, d2-1), (t3, d3-1), (t4, d4-1)])

for i in range(4):
    for j in range(4):
        tnum, td = MATRIX[i][j]
        THIEVES_INFO[tnum] = (i, j, td)
        MATRIX[i][j] = tnum


TAG_POS = (0, 0)
TAG_DIR = THIEVES_INFO[MATRIX[0][0]][2]
THIEVES_INFO[MATRIX[0][0]] = 'DEAD'
ANSWER = MATRIX[0][0]
MATRIX[0][0] = 0

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

def in_range(x, y):
    return -1 < x < 4 and -1 < y < 4

def change_dir(d):
    return (d+1)%8

# 도둑 이동. tag_pos는 (x, y)
def thieves_move(matrix, thieves_info, tag_pos):
    for tid in range(1, 17):
        if thieves_info[tid] != 'DEAD':
            x, y, d = thieves_info[tid]
            nx, ny = x+dx[d], y+dy[d]
            impossible = False
            if not in_range(nx, ny) or (nx, ny) == tag_pos:
                impossible = True
                nd = d
                for _ in range(7):
                    nd = change_dir(nd)
                    nx, ny = x+dx[nd], y+dy[nd]
                    if in_range(nx, ny) and (nx, ny) != tag_pos:
                        impossible = False
                        d = nd
                        break
                    
            if not impossible and in_range(nx, ny) and (nx, ny) != tag_pos:
                # 이동 가능
                if matrix[nx][ny] == 0:
                    matrix[nx][ny] = tid
                    matrix[x][y] = 0
                    thieves_info[tid] = (nx, ny, d)
                else: # 다른 도둑이 있었다면 자리 교환
                    next_tid = matrix[nx][ny]
                    next_d = thieves_info[next_tid][2]
                    matrix[nx][ny] = tid
                    thieves_info[tid] = (nx, ny, d)
                    matrix[x][y] = next_tid
                    thieves_info[next_tid] = (x, y, next_d)

# dfs
def game_play(tag_pos, tag_dir, matrix, thieves_info, score):
    global ANSWER

    if score > ANSWER:
        ANSWER = score

    # 도둑 이동
    thieves_move(matrix, thieves_info, tag_pos)

    # 술래 이동
    for i in range(1, 4):
        # print(tag_dir)
        nx, ny = tag_pos[0]+dx[tag_dir]*i, tag_pos[1]+dy[tag_dir]*i
        if in_range(nx, ny) and matrix[nx][ny] > 0:
            new_matrix = deepcopy(matrix)
            new_thieves_info = deepcopy(thieves_info)

            # 도둑 잡기
            new_tag_pos = (nx, ny)
            dead_tid = new_matrix[nx][ny]
            new_tag_dir = new_thieves_info[dead_tid][2]
            new_thieves_info[dead_tid] = 'DEAD'
            new_matrix[nx][ny] = 0
            new_score = score + dead_tid

            game_play(new_tag_pos, new_tag_dir, new_matrix, new_thieves_info, new_score)


from copy import deepcopy
# print(TAG_DIR)
# 현재 방향으로 최대 3번까지 가볼 수 있으므로 모두 시도.
answer = ANSWER

thieves_move(MATRIX, THIEVES_INFO, TAG_POS)

for i in range(1, 4):
    nx, ny = TAG_POS[0]+dx[TAG_DIR]*i, TAG_POS[1]+dy[TAG_DIR]*i
    if in_range(nx, ny) and MATRIX[nx][ny] > 0:
        # MATRIX[nx][ny] 에 있는 도둑을 잡았다고 가정하고 진행해 보기
        new_matrix = deepcopy(MATRIX)
        new_thieves_info = deepcopy(THIEVES_INFO)

        # 도둑 잡기
        tag_pos = (nx, ny)
        dead_tid = new_matrix[nx][ny]
        tag_dir = new_thieves_info[dead_tid][2]
        score = answer + dead_tid
        new_thieves_info[dead_tid] = 'DEAD'
        new_matrix[nx][ny] = 0
        game_play(tag_pos, tag_dir, new_matrix, new_thieves_info, score)

print(ANSWER)