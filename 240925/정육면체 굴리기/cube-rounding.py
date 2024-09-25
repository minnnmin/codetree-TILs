N, M, X, Y, K = map(int, input().split())
matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

move_order = list(map(int, input().split()))

# 정육면체 6면에 쓰인 숫자
down = 0
front = 0
right = 0
up = 0
left = 0
back = 0

def move_east():
    global down, front, right, up, left, back
    # 주사위 숫자 갱신
    tmp = down
    down = right
    right = up
    up = left
    left = tmp

def move_west():
    global down, front, right, up, left, back
    tmp = left
    left = up
    up = right
    right = down
    down = tmp

def move_north():
    global down, front, right, up, left, back
    tmp = back
    back = up
    up = front
    front = down
    down = tmp

def move_south():
    global down, front, right, up, left, back
    tmp = down
    down = front
    front = up
    up = back
    back = tmp


for mo in move_order:
    if mo == 1: # east
        if Y+1 < M:
            move_east()
            Y += 1
    elif mo == 2: # west
        if Y-1 > -1:
            move_west()
            Y -= 1
    elif mo == 3: # north
        if X-1 > -1:
            move_north()
            X -= 1
    elif mo == 4: # south
        if X+1 < N:
            move_south()
            X += 1 
    if matrix[X][Y] != 0:
        down = matrix[X][Y]
        matrix[X][Y] = 0
    print(up)