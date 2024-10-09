from copy import deepcopy

N = int(input())
MATRIX = [list(map(int, input().split())) for _ in range(N)]

ANSWER = 0

# 주어진 방향대로 돌려서 최대 점수 갱신
def play_game(dlist):
    global ANSWER

    new_matrix = deepcopy(MATRIX)

    for now_d in dlist:
        if now_d == 0: # 위
            # 숫자 합치기
            for col in range(N):
                now_num = new_matrix[0][col]
                cnt = 1
                for row in range(1, N):
                    if new_matrix[row][col] == 0:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    elif new_matrix[row][col] == now_num and cnt == 1:
                        new_matrix[row-1][col] = now_num*2
                        new_matrix[row][col] = 0
                        cnt = 2
                    elif new_matrix[row][col] == now_num and cnt == 2:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    else:
                        now_num = new_matrix[row][col]
                        cnt = 1
            # 숫자 이동
            for col in range(N):
                cnt = 0
                for row in range(N):
                    if new_matrix[row][col] == 0:
                        cnt += 1
                        continue
                    if cnt > 0:
                        new_matrix[row-cnt][col] = new_matrix[row][col]
                        new_matrix[row][col] = 0
        elif now_d == 1: # 오
            # 숫자 합치기
            for row in range(N):
                now_num = new_matrix[row][N-1]
                cnt = 1
                for col in range(N-2, -1, -1):
                    if new_matrix[row][col] == 0:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    elif new_matrix[row][col] == now_num and cnt == 1:
                        new_matrix[row][col+1] = now_num*2
                        new_matrix[row][col] = 0
                        cnt = 2
                    elif new_matrix[row][col] == now_num and cnt == 2:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    else:
                        now_num = new_matrix[row][col]
                        cnt = 1
            # 숫자 이동
            for row in range(N):
                cnt = 0
                for col in range(N-1, -1, -1):
                    if new_matrix[row][col] == 0:
                        cnt += 1
                        continue
                    if cnt > 0:
                        new_matrix[row][col+cnt] = new_matrix[row][col]
                        new_matrix[row][col] = 0

        elif now_d == 2: # 아래
            # 숫자 합치기
            for col in range(N):
                now_num = new_matrix[N-1][col]
                cnt = 1
                for row in range(N-2, -1, -1):
                    if new_matrix[row][col] == 0:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    elif new_matrix[row][col] == now_num and cnt == 1:
                        new_matrix[row+1][col] = now_num*2
                        new_matrix[row][col] = 0
                        cnt = 2
                    elif new_matrix[row][col] == now_num and cnt == 2:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    else:
                        now_num = new_matrix[row][col]
                        cnt = 1
            # 숫자 이동
            for col in range(N):
                cnt = 0
                for row in range(N-1, -1, -1):
                    if new_matrix[row][col] == 0:
                        cnt += 1
                        continue
                    if cnt > 0:
                        new_matrix[row+cnt][col] = new_matrix[row][col]
                        new_matrix[row][col] = 0
        elif now_d == 3: # 왼
            # 숫자 합치기
            for row in range(N):
                now_num = new_matrix[row][0]
                cnt = 1
                for col in range(1, N):
                    if new_matrix[row][col] == 0:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    elif new_matrix[row][col] == now_num and cnt == 1:
                        new_matrix[row][col-1] = now_num*2
                        new_matrix[row][col] = 0
                        cnt = 2
                    elif new_matrix[row][col] == now_num and cnt == 2:
                        now_num = new_matrix[row][col]
                        cnt = 1
                    else:
                        now_num = new_matrix[row][col]
                        cnt = 1
            # 숫자 이동
            for row in range(N):
                cnt = 0
                for col in range(N):
                    if new_matrix[row][col] == 0:
                        cnt += 1
                        continue
                    if cnt > 0:
                        new_matrix[row][col-cnt] = new_matrix[row][col]
                        new_matrix[row][col] = 0

    max_num = 0
    for i in range(N):
        for j in range(N):
            if new_matrix[i][j] > max_num:
                max_num = new_matrix[i][j]
    if max_num > ANSWER:
        ANSWER = max_num


for d1 in range(4):
    for d2 in range(4):
        for d3 in range(4):
            for d4 in range(4):
                for d5 in range(4):
                    play_game((d1, d2, d3, d4, d5))

print(ANSWER)