'''
1) 인접블럭 높이가 1 초과면 X
2) 인접블럭 높이가 1 이하면
    2-1) 높이가 모두 같으면 O
    2-2) 가다가 막히면(높이 다르면) 길이 L짜리 경사로 놓을 수 있는지 확인
        2-2-1) 동일 높이가 L개 이상이면 O
        2-2-2) 동일 높이가 L개 이상이면 X
'''

N, L = map(int, input().split())
original_blocks = []
for _ in range(N):
    original_blocks.append(list(map(int, input().split())))

new_blocks = [] # 행렬 뒤집은 버전
for i in range(N):
    tmp = []
    for j in range(N):
        tmp.append(original_blocks[j][i])
    new_blocks.append(tmp)

def check_blocks(blocks): # 행 검사
    available = 0

    for b in blocks:
        ex = -1
        cont_block_cnt = 1 # 연속된 동일한 높이 블럭 길이
        will_cont_block_cnt = 0 # 현재까지 연속된 동일 블럭 개수(내리막에 사용)
        down = False
        visited = [False] * N
        for i in range(N):
            if i == 0:
                ex = b[i]
            else:
                if down:
                    if will_cont_block_cnt == L: # 경사로 설치 가능
                        visited[i - 1] = True
                        down = False
                        cont_block_cnt += 1
                        will_cont_block_cnt = 0
                if b[i] == ex:
                    if down:
                        will_cont_block_cnt += 1
                        visited[i] = True
                        if will_cont_block_cnt == L: # 경사로 설치 가능
                            down = False
                    else:
                        cont_block_cnt += 1
                else:
                    if b[i] - ex > 1: # 오르막
                        break
                    elif ex - b[i] > 1: # 내리막
                        break
                    elif b[i] - ex == 1: # 오르막 # 경사로 놓을 수 있는지 확인
                        if cont_block_cnt >= L and not visited[i - 1]: # 가능
                            ex = b[i]
                            cont_block_cnt = 1
                        else:
                            break
                    elif ex - b[i] == 1: # 내리막 # 경사로 놓을 수 있는지 확인해야 하므로 플래그 설정
                        ex = b[i]
                        cont_block_cnt = 0
                        will_cont_block_cnt += 1
                        down = True
            if i == N-1:
                if not down:
                    available += 1
                else:
                    if will_cont_block_cnt == L:
                        available += 1
                        print('2.', b)
                    
    return available

print(check_blocks(original_blocks) + check_blocks(new_blocks))