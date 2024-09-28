N = int(input())
DUST = [list(map(int, input().split())) for _ in range(N)]
DUST_OUT = 0 # 격자 밖 먼지 합

tmp = [1, 1]
for i in range(2, N):
    tmp.append(i)
    tmp.append(i)
tmp.append((N-1))
# tmp [1, 1, 2, 2, 3, 3, 4, 4, 4]

order_list = []
for i in range(len(tmp)):
    order_list.append((i%4, tmp[i]))

# order_list
# [(0, 1), (1, 1), (2, 2), (3, 2), (0, 3), (1, 3), (2, 4), (3, 4), (0, 4)]


# 좌, 하, 우, 상
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


def in_range(x, y):
    return -1 < x < N and -1 < y < N


# 각 방향으로 움직였을 때, 먼지를 이동시켜서 DUST_OUT 값 초기화
# d 방향으로 움직여 (x, y)로 온 상태
# 마지막에 DUST[x][y]값은 0으로 초기화
def move_dust(x, y, d):
    global DUST_OUT
    dust = DUST[x][y]

    # a를 제외한 나머지 9곳으로 이동한 먼지 합
    sum_but_a = int(dust*0.01)*2 + int(dust*0.02)*2 + int(dust*0.07)*2 + int(dust*0.05) + int(dust*0.1)*2
    # a로 이동한 먼지
    a_dust = dust - sum_but_a

    if d == 0: # 좌
        # a 세팅
        if in_range(x, y-1):
            DUST[x][y-1] += a_dust
        else:
            DUST_OUT += a_dust
        # 1%
        if in_range(x-1, y+1):
            DUST[x-1][y+1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        if in_range(x+1, y+1):
            DUST[x+1][y+1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        # 2%
        if in_range(x-2, y):
            DUST[x-2][y] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        if in_range(x+2, y):
            DUST[x+2][y] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        # 5%
        if in_range(x, y-2):
            DUST[x][y-2] += int(dust*0.05)
        else:
            DUST_OUT += int(dust*0.05)
        # 7%
        if in_range(x-1, y):
            DUST[x-1][y] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        if in_range(x+1, y):
            DUST[x+1][y] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        # 10%
        if in_range(x-1, y-1):
            DUST[x-1][y-1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
        if in_range(x+1, y-1):
            DUST[x+1][y-1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
    elif d == 1: # 하
        # a 세팅
        if in_range(x+1, y):
            DUST[x+1][y] += a_dust
        else:
            DUST_OUT += a_dust
        # 1%
        if in_range(x-1, y-1):
            DUST[x-1][y-1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        if in_range(x-1, y+1):
            DUST[x-1][y+1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        # 2%
        if in_range(x, y-2):
            DUST[x][y-2] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        if in_range(x, y+2):
            DUST[x][y+2] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        # 5%
        if in_range(x+2, y):
            DUST[x+2][y] += int(dust*0.05)
        else:
            DUST_OUT += int(dust*0.05)
        # 7%
        if in_range(x, y-1):
            DUST[x][y-1] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        if in_range(x, y+1):
            DUST[x][y+1] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        # 10%
        if in_range(x+1, y-1):
            DUST[x+1][y-1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
        if in_range(x+1, y+1):
            DUST[x+1][y+1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
    elif d == 2: # 우
        # a 세팅
        if in_range(x, y+1):
            DUST[x][y+1] += a_dust
        else:
            DUST_OUT += a_dust
        # 1%
        if in_range(x-1, y-1):
            DUST[x-1][y-1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        if in_range(x+1, y-1):
            DUST[x+1][y-1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        # 2%
        if in_range(x-2, y):
            DUST[x-2][y] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        if in_range(x+2, y):
            DUST[x+2][y] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        # 5%
        if in_range(x, y+2):
            DUST[x][y+2] += int(dust*0.05)
        else:
            DUST_OUT += int(dust*0.05)
        # 7%
        if in_range(x-1, y):
            DUST[x-1][y] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        if in_range(x+1, y):
            DUST[x+1][y] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        # 10%
        if in_range(x-1, y+1):
            DUST[x-1][y+1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
        if in_range(x+1, y+1):
            DUST[x+1][y+1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1) 
    elif d == 3: # 상
        # a 세팅
        if in_range(x-1, y):
            DUST[x-1][y] += a_dust
        else:
            DUST_OUT += a_dust
        # 1%
        if in_range(x+1, y-1):
            DUST[x+1][y-1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        if in_range(x+1, y+1):
            DUST[x+1][y+1] += int(dust*0.01)
        else:
            DUST_OUT += int(dust*0.01)
        # 2%
        if in_range(x, y-2):
            DUST[x][y-2] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        if in_range(x, y+2):
            DUST[x][y+2] += int(dust*0.02)
        else:
            DUST_OUT += int(dust*0.02)
        # 5%
        if in_range(x-2, y):
            DUST[x-2][y] += int(dust*0.05)
        else:
            DUST_OUT += int(dust*0.05)
        # 7%
        if in_range(x, y-1):
            DUST[x][y-1] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        if in_range(x, y+1):
            DUST[x][y+1] += int(dust*0.07)
        else:
            DUST_OUT += int(dust*0.07)
        # 10%
        if in_range(x-1, y-1):
            DUST[x-1][y-1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1)
        if in_range(x-1, y+1):
            DUST[x-1][y+1] += int(dust*0.1)
        else:
            DUST_OUT += int(dust*0.1) 

    DUST[x][y] = 0

now_x, now_y = N//2, N//2
for d, size in order_list:
    for _ in range(size):
        now_x += dx[d]
        now_y += dy[d]
        move_dust(now_x, now_y, d)
        # for _ in DUST:
        #     print(_)
        # print()        
print(DUST_OUT)